import torch
import torch.nn as nn
import numpy as np
from time import perf_counter_ns
import matplotlib.pyplot as plt



class Reconstruction(nn.Module):
    """
    basic reconstruction steps without dispersion correction or background subtraction, to transform spectra into images
    """
    def __init__(self, a_len, device) -> None:
        super().__init__()
        self.alen = a_len
        self.window = torch.hann_window(self.alen).to(device)

    def forward(self, S, log=True, mag=True, one_sided=True):
        # t0 = perf_counter_ns()

        # spectral shaping
        S = S * self.window

        # FFT
        B = torch.fft.fft(S, n=2*self.alen, dim=-1) # FFT along last dimension

        if one_sided:
            B = B[...,:self.alen]

        # mag & log
        if mag:
            B = torch.abs(B)
        if log:
            B = torch.log10(B)

        # final scaling

        # torch.cuda.synchronize()
        # print("Elapsed [ms]:", (perf_counter_ns()-t0)/1e6)
        return B
    

if __name__ == "__main__":

    DEVICE = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu") # detects available device (GPU or CPU)

    S = np.random.rand(512,1024)

    with torch.no_grad(): # Tell pytorch to not track gradients. This is optional and may reduce memory demands (see documentation)

        # move to torch, add (pseudo-) batch and channel dimension (size = BxCx)  
        # --> this may strictly not be necessary, important is that (currently) FFT is performed along final dimension
        S_torch = torch.from_numpy(S).unsqueeze_(0).unsqueeze_(0)

        S_torch = S_torch.to(DEVICE) # moves Tensor to GPU, if available

        Recon = Reconstruction(a_len = S_torch.size(-1), device=DEVICE)# create a reconstruction object

        B_torch = Recon(S_torch, log=True, mag=True, one_sided=True) # call to Recon.forward(...)

        B = B_torch.squeeze().cpu().numpy() # moves Tensor to CPU and converts it back to numpy array

    fig, axs = plt.subplots(1,2)
    axs[0].imshow(S)
    axs[1].imshow(B)
    plt.show()


