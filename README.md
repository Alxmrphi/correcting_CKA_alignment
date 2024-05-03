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
when debiased CKA detects stimuli-driven alignment

## Biased CKA on Random Matrices
One issue we highlight is that CKA without the debiasing step can be artificially driven up to its maximum by purely increasing the ratio of features to samples. This occurs in random matrices that have no shared structure. However, methods to correct for this bias in CKA (debiased CKA & RV2) correctly determine that no alignment is present as the feature dimensionality increases from a fixed number of samples (rows). The issue with biased CKA is not present in the typical scenario of tall, skinny matrices. However, in the realm of neural data, we often see very high-dimensional feature vectors over a limited number of samples. It's in this scenario that biased CKA has the potential to suggest that alignment exists when this is not the case. 

<img src="https://github.com/Alxmrphi/correcting_CKA_alignment/blob/main/figures/fig1-random.png" width="700" height="390">

## ResNet18 and CORnet-S 
We next demonstrate the alignment scores between fMRI and MEG data from the THINGS project with layer activations from two CNN models: ResNet18 and CORnet-S. We sample random matrices equal to the size of the true V1 region of interest (in fMRI) and occipital responses (in MEG), in addition to measuring the responses to the true stimuli as well as shuffled data. If V1 data were used in a real experiment that had noise-like properties similar to random noise, biased CKA would return very high values and incorrectly suggest alignment exists when none is present. We further see that by disrupting the stimuli-response pairs (via shuffling), similar biased CKA values are detected. It's only when using debiased CKA as a measurement that we: (i) correctly detect absence of alignment with random matrices, (ii) correctly detect absence of alignment when stimuli-response pairs are shuffled and (iii) correctly detect alignment when the neural responses are associated with the correct stimuli. For this reason, we argue that when measuring (or inducing) brain-like representations into neural networks, debiased CKA appears to be the better metric to use.

<img src="https://github.com/Alxmrphi/correcting_CKA_alignment/blob/main/figures/fig2-resnet_cornet.png" width="700" height="590">

# Full Shuffling (ResNet18)
Please see the paper for detailed explanations of these results. 

<img src="https://github.com/Alxmrphi/correcting_CKA_alignment/blob/main/figures/fig3-resnet_rois.png" width="700" height="390">

## Partial Shuffling (ResNet18)
Please see the paper for detailed explanations of these results. 

<img src="https://github.com/Alxmrphi/correcting_CKA_alignment/blob/main/figures/fig5-partial_shuffle.png" width="700" height="390">

# Misc

The neural data used in this project were released as part of the THINGS dataset. However, we received early access to this dataset and feature extraction proceeded on a version, which has since been updated and released as part of the THINGS initiative. If downloading the corresponding data to reproduce our results, the archived version of the MEG / fMRI data is the one that our code runs on. 
