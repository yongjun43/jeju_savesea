class CustomSatelliteCarDataset(Dataset):
    def __init__(self, img_dir, label_dir, transform=None):
        self.img_dir = img_dir
        self.label_dir = label_dir
        self.transform = transform  # 변환은 이미 ToTensor와 Normalize를 포함합니다.
        self.images = [os.path.join(img_dir, file) for file in os.listdir(img_dir) if file.endswith('.jpg')]

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_path = self.images[idx]
        image = Image.open(img_path).convert('RGB')  # PIL 이미지로 로드하고 RGB로 변환

        if self.transform:
            image = self.transform(image)  # ToTensor 및 기타 변환 적용

        label_path = os.path.join(self.label_dir, os.path.splitext(os.path.basename(img_path))[0] + '.txt')
        labels = self.read_label_file(label_path)

        return image, labels

    def read_label_file(self, file_path):
        max_boxes = 50  # 한 이미지에 최대 50개의 바운딩 박스를 가정
        boxes = []
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                # 부족한 부분을 0으로 채워서 항상 5개 요소를 갖도록 합니다.
                while len(parts) < 5:
                    parts.append('0.0')  # x, y, width, height, class_id 중 누락된 값을 0으로 채움
                box = [float(x) for x in parts[:5]]  # 첫 5개 요소만 사용 (class_id, x, y, width, height)
                boxes.append(torch.tensor(box, dtype=torch.float32))

        # 레이블 수가 max_boxes보다 적은 경우, 남은 공간을 0으로 채워 고정된 크기를 유지합니다.
        while len(boxes) < max_boxes:
            boxes.append(torch.zeros(5, dtype=torch.float32))  # '빈' 바운딩 박스 추가

        return torch.stack(boxes)[:max_boxes]  # 첫 번째 max_boxes 개의 박스만 반환하여 크기를 고정합니다.




def collate_fn(batch):
    images, labels = zip(*batch)
    images = torch.stack(images, 0)  # 이미지들을 하나의 배치로 합칩니다.
    # 모든 레이블에 대해 가장 긴 레이블 길이를 찾아 해당 길이만큼 패딩합니다.
    max_boxes = max(len(label) for label in labels)
    padded_labels = [torch.cat([label, torch.zeros(max_boxes - len(label), 5)]) if len(label) < max_boxes else label for label in labels]
    labels = torch.stack(padded_labels, 0)
    return images, labels


train_dataset = CustomSatelliteCarDataset(
    img_dir='/content/drive/MyDrive/jeju/Satellite_car/train/images',
    label_dir='/content/drive/MyDrive/jeju/Satellite_car/train/labels',
    transform=transform
)

train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True, collate_fn=collate_fn)
