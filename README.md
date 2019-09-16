
# Energy Conservation in Disks Utilizing Related Data Concentration

* The project aims at conserving the energy in the RAID disks by using the related data concentration.

* The RAID disks were emulated using the DiskSim Simulation Environment by making small modifications.

* The web server disk usage traces were collected from the FIU's Computer Science web, email and dev servers.

* These web traces were used to simulate the real-world file access by developing an interface to mimic the functionality of a File System like moving the files, allocating memory and keeping track of empty disk spaces.

* Reinforcement learning algorithm was used to cluster related files in the same RAID Disks based on the written policy.

* Clustering of files helps in conserving energy by spinning down the unused disks.
