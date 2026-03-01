
<!-- ----------------------------------------------------------------------- -->
<!--                             WITH DEPTH HEAD                             -->
<!-- ----------------------------------------------------------------------- -->

GPU Memory before load_backbone: [GPU-LEAK ?] Allocated: 0.00GB (Peak: 0.00GB) | Reserved: 0.00GB (Peak: 0.00GB)
GPU Memory impact of load_backbone: [GPU-LEAK ?] Allocated: 0.08GB (Peak: 0.08GB) | Reserved: 0.11GB (Peak: 0.11GB)


GPU Memory before create_depther: [GPU-LEAK ?] Allocated: 0.08GB (Peak: 0.08GB) | Reserved: 0.11GB (Peak: 0.11GB)
GPU Memory impact of create_depther: [GPU-LEAK ?] Allocated: 0.00GB (Peak: 0.00GB) | Reserved: 0.00GB (Peak: 0.00GB)

GPU Memory Usage Before depth image: [GPU-LEAK ?] Allocated: 0.14GB (Peak: 0.14GB) | Reserved: 0.15GB (Peak: 0.15GB)
batch.shape = torch.Size([1, 3, 480, 640]) batch.dtype = torch.float32
GPU Memory Usage After depth image: [GPU-LEAK ?] Allocated: 0.15GB (Peak: 0.55GB) | Reserved: 0.96GB (Peak: 0.96GB)


GPU Memory Usage Before batch processing of N=8: [GPU-LEAK ?] Allocated: 0.15GB (Peak: 0.55GB) | Reserved: 0.96GB (Peak: 0.96GB)
batch.shape = torch.Size([8, 3, 480, 640]) batch.dtype = torch.float32
GPU Memory Usage After batch processing of N=8: [GPU-LEAK ?] Allocated: 0.18GB (Peak: 5.03GB) | Reserved: 8.21GB (Peak: 8.21GB)


GPU Memory Usage Before batch processing of N=16: [GPU-LEAK ?] Allocated: 0.18GB (Peak: 5.03GB) | Reserved: 8.21GB (Peak: 8.21GB)
batch.shape = torch.Size([16, 3, 480, 640]) batch.dtype = torch.float32
GPU Memory Usage After batch processing of N=16: [GPU-LEAK ?] Allocated: 0.22GB (Peak: 9.92GB) | Reserved: 16.30GB (Peak: 16.30GB)


GPU Memory Usage Before batch processing of N=32: [GPU-LEAK ?] Allocated: 0.22GB (Peak: 9.92GB) | Reserved: 16.30GB (Peak: 16.30GB)
batch.shape = torch.Size([32, 3, 480, 640]) batch.dtype = torch.float32
GPU Memory Usage After batch processing of N=32: [GPU-LEAK ?] Allocated: 0.29GB (Peak: 13.23GB) | Reserved: 15.34GB (Peak: 18.58GB)


<!-- ----------------------------------------------------------------------- -->
<!--                              Backbone only                              -->
<!-- ----------------------------------------------------------------------- -->
GPU Memory before load_backbone: [GPU-LEAK ?] Allocated: 0.00GB (Peak: 0.00GB) | Reserved: 0.00GB (Peak: 0.00GB)
GPU Memory impact of load_backbone: [GPU-LEAK ?] Allocated: 0.08GB (Peak: 0.08GB) | Reserved: 0.11GB (Peak: 0.11GB)


GPU Memory Usage Before depth image: [GPU-LEAK ?] Allocated: 0.08GB (Peak: 0.08GB) | Reserved: 0.11GB (Peak: 0.11GB)
batch.shape = torch.Size([1, 3, 476, 630]) batch.dtype = torch.float32
GPU Memory Usage After depth image: [GPU-LEAK ?] Allocated: 0.10GB (Peak: 0.12GB) | Reserved: 0.15GB (Peak: 0.15GB)

GPU Memory Usage Before batch processing of N=8: [GPU-LEAK ?] Allocated: 0.10GB (Peak: 0.12GB) | Reserved: 0.15GB (Peak: 0.15GB)
batch.shape = torch.Size([8, 3, 476, 630]) batch.dtype = torch.float32
GPU Memory Usage After batch processing of N=8: [GPU-LEAK ?] Allocated: 0.14GB (Peak: 0.31GB) | Reserved: 0.41GB (Peak: 0.41GB)

GPU Memory Usage Before batch processing of N=16: [GPU-LEAK ?] Allocated: 0.14GB (Peak: 0.31GB) | Reserved: 0.41GB (Peak: 0.41GB)
batch.shape = torch.Size([16, 3, 476, 630]) batch.dtype = torch.float32
GPU Memory Usage After batch processing of N=16: [GPU-LEAK ?] Allocated: 0.18GB (Peak: 0.55GB) | Reserved: 0.87GB (Peak: 0.87GB)

GPU Memory Usage Before batch processing of N=32: [GPU-LEAK ?] Allocated: 0.18GB (Peak: 0.55GB) | Reserved: 0.87GB (Peak: 0.87GB)
batch.shape = torch.Size([32, 3, 476, 630]) batch.dtype = torch.float32
GPU Memory Usage After batch processing of N=32: [GPU-LEAK ?] Allocated: 0.27GB (Peak: 1.01GB) | Reserved: 1.79GB (Peak: 1.79GB)

GPU Memory Usage Before batch processing of N=64: [GPU-LEAK ?] Allocated: 0.27GB (Peak: 1.01GB) | Reserved: 1.79GB (Peak: 1.79GB)
batch.shape = torch.Size([64, 3, 476, 630]) batch.dtype = torch.float32
GPU Memory Usage After batch processing of N=64: [GPU-LEAK ?] Allocated: 0.45GB (Peak: 1.92GB) | Reserved: 3.62GB (Peak: 3.62GB)

GPU Memory Usage Before batch processing of N=128: [GPU-LEAK ?] Allocated: 0.45GB (Peak: 1.92GB) | Reserved: 3.62GB (Peak: 3.62GB)
batch.shape = torch.Size([128, 3, 476, 630]) batch.dtype = torch.float32
GPU Memory Usage After batch processing of N=128: [GPU-LEAK ?] Allocated: 0.80GB (Peak: 3.75GB) | Reserved: 7.28GB (Peak: 7.28GB)

GPU Memory Usage Before batch processing of N=256: [GPU-LEAK ?] Allocated: 0.80GB (Peak: 3.75GB) | Reserved: 7.28GB (Peak: 7.28GB)
batch.shape = torch.Size([256, 3, 476, 630]) batch.dtype = torch.float32
GPU Memory Usage After batch processing of N=256: [GPU-LEAK ?] Allocated: 1.51GB (Peak: 7.40GB) | Reserved: 14.60GB (Peak: 14.60GB

GPU Memory Usage Before batch processing of N=512: [GPU-LEAK ?] Allocated: 1.51GB (Peak: 7.40GB) | Reserved: 14.60GB (Peak: 14.60GB)
batch.shape = torch.Size([512, 3, 476, 630]) batch.dtype = torch.float32
GPU Memory Usage After batch processing of N=512: [GPU-LEAK ?] Allocated: 2.93GB (Peak: 14.70GB) | Reserved: 18.64GB (Peak: 18.64GB)