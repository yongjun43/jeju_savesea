#cocodataset

train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)

# 모델 및 손실 함수, 옵티마이저 초기화
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = HSPYOLOv8(num_classes=6).to(device)
criterion = YOLOLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 훈련 루프
num_epochs = 10
for epoch in range(num_epochs):
    model.train(epochs=20)
    running_loss = 0.0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
    print(f'Epoch {epoch+1}/{num_epochs}, Loss: {running_loss/len(train_loader)}')
