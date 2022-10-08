# 網路程式設計
## Lab 4 – Concurrent Server
請修改 Lab 2 的 Server 程式，當 Server 的 main thread 收到 Client 的連線建立訊息後即產生一個新的 thread 與 Client 繼續溝通。如此 Server 可以再等待新的 Client 的連線，以同時處理多個 Client 的連線要求。