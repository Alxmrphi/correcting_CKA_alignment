# Correcting Biased Centered Kernel Alignment Measures in Biological and Artificial Neural Networks (Re-Align, ICLR 2024)

[Paper](https://arxiv.org/abs/2405.01012)

[Poster](https://github.com/Alxmrphi/correcting_CKA_alignment/blob/main/ReAlign_ICLR_AlexMurphy-01.png)


# Abstract 

Centred Kernel Alignment (CKA) has recently emerged as a popular metric to
compare activations from biological and artificial neural networks (ANNs) in or-
der to quantify the alignment between internal representations derived from stim-
uli sets (e.g. images, text, video) that are presented to both systems (Sucholutsky
et al., 2023; Han et al., 2023). In this paper we highlight issues that the commu-
nity should take into account if using CKA as an alignment metric with neural
data. Neural data are in the low-data high-dimensionality domain, which is one
of the cases where (biased) CKA results in high similarity scores even for pairs of
random matrices. Using fMRI and MEG data from the THINGS project (Hebart
et al., 2023), we show that if biased CKA is applied to representations of different
sizes in the low-data high-dimensionality domain, they are not directly compa-
rable due to biased CKA’s sensitivity to differing feature-sample ratios and not
stimuli-driven responses. This situation can arise both when comparing a pre-
selected area of interest (e.g. ROI) to multiple ANN layers, as well as when deter-
mining to which ANN layer multiple regions of interest (ROIs) / sensor groups of
different dimensionality are most similar. We show that biased CKA can be artifi-
cially driven to its maximum value when using independent random data of differ-
ent sample-feature ratios. We further show that shuffling sample-feature pairs of
real neural data does not drastically alter biased CKA similarity in comparison to
unshuffled data, indicating an undesirable lack of sensitivity to stimuli-driven neu-
ral responses. Positive alignment of true stimuli-driven responses is only achieved
by using debiased CKA. Lastly, we report findings that suggest biased CKA is
sensitive to the inherent structure of neural data, only differing from shuffled data
when debiased CKA detects stimuli-driven alignment.

## What's the issue?
<img src="https://github.com/Alxmrphi/correcting_CKA_alignment/blob/main/figures/whats_the_issue.png" width="500" height="290">
You have some brain data that was recorded in response to a participant perceiving some stimuli (e.g. looking at an image) and you want to know if a vision model's activations of the same image are aligned. You've been reading up on recent research in the field and see many people using Centered Kernel Alignment (CKA) to measure this. You want to compare a layer across multiple ROIs (i.e. is CNN layer 4 more aligned with hV4 or PPA?) or you might want to look at which layer of a CNN is most aligned to a fixed ROI (i.e. which of the CNN layers is most like FFA in my data?) We present here some details about using out-of-the-box (biased) CKA that might lead you astray in the hope that people don't make the same mistakes as the ones we originally made. However, a very simple fix is present that corrects for many of the issues we note and we encourage people to use the debiased version of CKA for such reasons.

## Biased CKA on Random Matrices
One issue we highlight is that CKA without the debiasing step can be artificially driven up to its maximum by purely increasing the ratio of features to samples. This occurs in random matrices that have no shared structure. However, methods to correct for this bias in CKA (debiased CKA & RV2) correctly determine that no alignment is present as the feature dimensionality increases from a fixed number of samples (rows). The issue with biased CKA is not present in the typical scenario of tall, skinny matrices. However, in the realm of neural data, we often see very high-dimensional feature vectors over a limited number of samples. It's in this scenario that biased CKA has the potential to suggest that alignment exists when this is not the case. 

<img src="https://github.com/Alxmrphi/correcting_CKA_alignment/blob/main/figures/fig1-random.png" width="700" height="390">

## ResNet18 and CORnet-S 
We next demonstrate the alignment scores between fMRI and MEG data from the THINGS project with layer activations from two CNN models: ResNet18 and CORnet-S. We sample random matrices equal to the size of the true V1 region of interest (in fMRI) and occipital responses (in MEG), in addition to measuring the responses to the true stimuli as well as shuffled data. If V1 data were used in a real experiment that had noise-like properties similar to random noise, biased CKA would return very high values and incorrectly suggest alignment exists when none is present. We further see that by disrupting the stimuli-response pairs (via shuffling), similar biased CKA values are detected. It's only when using debiased CKA as a measurement that we: (i) correctly detect absence of alignment with random matrices, (ii) correctly detect absence of alignment when stimuli-response pairs are shuffled and (iii) correctly detect alignment when the neural responses are associated with the correct stimuli. For this reason, we argue that when measuring (or inducing) brain-like representations into neural networks, debiased CKA appears to be the better metric to use.

<img src="https://github.com/Alxmrphi/correcting_CKA_alignment/blob/main/figures/fig2-resnet_cornet.png" width="700" height="590">

# Full Shuffling (ResNet18)
In order to better compare the biased vs debiased alignment results across various ROIs for one model (we present ResNet18 results below; see paper for CORnet-S results). We first want to draw your attention to the purple and green bars in the plot below. This is the alignment that results from using biased CKA on original data (purple) vs when the rows of the fMRI data have been shuffled (green). You can see a striking similarity between the bars across all ResNet18 layers and many fMRI ROIs. If the brain is shuffled, this means that the CNN activations and the brain response are to completely different images. However, the alignment is very similar. This is an undesirable property because it shows us that what is being measured is not directly related to the properties of the stimulus itself. When using debiased CKA, we see this behaviour change dramatically and no alignment is present when shuffling occurs, which is what we would expect in a good alignment metric. We see smaller responses that appear to be driven by the true properties of the stimulus. We further note that only when using debiased CKA is there more alignment between lower visual regions and lower CNN layers (an oft-cited observation in the literature). As we look at regions further up the visual hierarchy, more middle-to-later layers show increased patterns of alignment. We further observe that only in cases where debiased CKA reveals positive stimuli-driven alignment is there an increase in biased CKA alignment (purple) over the shuffled data (green). This suggests that biased CKA also detects stimuli-driven alignment, but only in addition to alignment also shared by shuffled fMRI data. Therefore, biased CKA alone is a measurement that can't be simply separated from a generalised response and could lead to incorrect conclusions w.r.t. stimuli-driven alignment. In short, when debiased CKA is zero, biased CKA returns the same result for unshuffled and shuffled data. Biased CKA only returns a higher value when the debiased CKA metric detects stimuli-driven alignment (by approximately the same amount). 

<img src="https://github.com/Alxmrphi/correcting_CKA_alignment/blob/main/figures/fig3-resnet_rois.png" width="700" height="390">

## Partial Shuffling (ResNet18)
In order to dig a bit deeper into the effect on shuffling on the alignment using both biased and debiased CKA, we hypothesised that as you gradually increase the proportion of shuffled data, the debiased CKA value should gradually diminish, as less stimuli-driven signal is present in the data. Conversely, we expected that no effect would be present when using the biased CKA results (i.e. increasing the amount of shuffling does not disrupt the reported alignment) in cases where debiased CKA doesn't detect any stimuli-driven alignment. When debiased CKA does detect stimuli-driven alignment and shuffling is introduced, the biased CKA value will decrease in tandem. To examine this we took V1 (top row) and left-PPA (bottom row) and three early layers from ResNet18. We saw above (in Full Shuffling) that there is debiased CKA alignment in V1 but not in left-PPA. As we increase the percentage of shuffling, the debiased (and biased) CKA alignment drops as we would expect. In regions where there is no stimuli-driven alignment detected, increasing the percentage of shuffling has no effect. This shows that the alignment values reported with biased CKA are not driven by the stimuli but rather to what we hypothesise is a more generalised response to the fMRI data.

<img src="https://github.com/Alxmrphi/correcting_CKA_alignment/blob/main/figures/fig5-partial_shuffle.png" width="700" height="390">

# Misc

The neural data used in this project were released as part of the THINGS dataset. However, we received early access to this dataset and feature extraction proceeded on a version, which has since been updated and released as part of the THINGS initiative. If downloading the corresponding data to reproduce our results, the archived version of the MEG / fMRI data is the one that our code runs on. This is part of a suite of results in an ongoing research paradigm and we intend to continue publishing more findings on this and related areas in the future. Stay tuned!
