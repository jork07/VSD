# About This Repository
This repository contains Python implementations of VSD(Video Storage in DNA). 
It mainly includes the following functions:
1. Video segmentation.
2. DNA encoding and decoding.
## Datasets
1. FoundingCeremony(https://www.youtube.com/watch?v=BIHPFgAulS0&list=PLm9ClEu2__aKddRGDNHR-vLFwW1E26zVv)
2. BandungConference(https://www.bilibili.com/video/BV18v41167CG/?spm_id_from=333.337.search-card.all.click&vd_source=4dccd6a2608eb13d97efd2ac532857be)
3. Macao1999(https://www.youtube.com/watch?v=cZ_E2BPghbc)
4. HongKong1997(https://www.youtube.com/watch?v=d2_Hl1DGnks)

We obtained other formats of videos in the paper from the sample website(https://filesamples.com/)
## Video Segmentation
Step 1: Open segmentation.py script(Confirm that you have installed ffmpeg);

Step 2: Choose a mp4 file, and set the output path & srgment duration;

Step 3: Run the script, it will will quickly complete video segmentation, and each video can be played separately.

## DNA transcoding
Step 1: Open VSD_codec.py script, drop down to line 250;

Step 2: Choose a mp4 segmentation file, and set the DNA file output path;

Step 3: Run the script,It will automatically perform a quaternary conversion and output a DNA sequence file in fasta format.
