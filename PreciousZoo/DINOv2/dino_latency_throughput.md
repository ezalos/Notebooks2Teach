GPU : RTX 4090
tensor_image.shape = torch.Size([N, 3, 476, 630])
tensor_image.dtype = torch.float32
N,Time (ms),Memory (GB),BACKBONE_SIZE

# Model Size : small
## Latency 1 Image 
- vRAM (Go) = 0.121 Go
- time (ms) = 17ms
## Throughput for largest n^2 batch under 8Go :
- Combien d'images en 1s ? = 122.1 im/s


# Model Size : base
## Latency 1 Image 
- vRAM (Go) = 0.39 Go
- time (ms) = 37ms
## Throughput for largest n^2 batch under 8Go :
- Combien d'images en 1s ? = 46.4 im/s


# Model Size : large
## Latency 1 Image 
- vRAM (Go) = 1.22 Go
- time (ms) = 81 ms
## Throughput for largest n^2 batch under 8Go :
- Combien d'images en 1s ? = 15.0 im/s


# Model Size : giant
## Latency 1 Image 
- vRAM (Go) = 4.42 Go
- time (ms) = 241 ms
## Throughput for largest n^2 batch under 8Go :
- Combien d'images en 1s ? = 5.4 im/s
