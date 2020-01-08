Ling 570 HW6 HMM
Daniel Campos
11/08/2018

## Approach/Structure used to store HMM in checkHMM
In my check HMM file I decided to use a dict. I did so mostly because I was crunched for time and I am most familiar with dicts and thus felt I could debug weird dict errors much better than I could debug weird single or double dimensional arrays.
I understand the approach produces a system that runs slower(On checking my 3g_hmm_0.2_0.3_0.5 it takes 1m48 on a older laptop ) which isnt ideal but I had a deadline to make!
I quickly noticed how slow this gets especially as we make the hmm larger. The 2g finishes in seconds and really highlights the effects of good programming.

Hopefully next time I am able to finish my hw assignment much earlier like I normally do and I can optimize and comment!
