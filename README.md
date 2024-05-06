# TRUBA HPC - SLURM SCRIPT GENERATOR
In the domain of High Performance Computing (HPC), efficiency is key. However, creating Slurm scripts manually can be time-consuming and error-prone, especially when dealing with multiple clusters each with their own requirements.

To address this, I've developed a Python script to automate the generation of Slurm scripts, making your workflow more efficient and reducing the risk of mistakes.

But why use this script when there are debug queues available? While debug queues can help, this tool helps eliminate potential errors in your scripts even before they are sent to the debug queues, saving you time and effort.

With this tool, you can easily integrate it into your existing codebase and customize it to suit your needs. So, let's have a look at what it does?

- Automatically fills the header part of the script. (You can leave the mail part as blank, since you may not want to get dozens/hundreds of emails, depending on the number of jobs)
- Checks whether the requested Truba cluster is available. For example, if your script requests "short" or "mid1" cluster, they will be automatically converted to the "hamsi" as per Truba's documentation (See: https://docs.truba.gov.tr/TRUBA/kullanici-el-kitabi/hesaplamakumeleri.html)
- Checks whether the requested job duration is inline with the maximum values defined by Truba. Also converts the invalid durations (eg. 0-00:15:75) to valid ones (eg. 0-00:16:15).
- Checks whether the requested node count is smaller than the physical capacity of Truba, and corrects any mistakes.
- Checks whether the requested core amount is inline with the requested node count and the selected cluster, and corrects any mistakes.

To - do (Probably in a distant future)
- Check CUDA clusters GPU vs minimum core number conditions.
- Ability to be able to check the available number of nodes for different clusters and offer alternative clusters while considering the initially requested core count and ram amount. 
