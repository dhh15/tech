---
title: "Exploring Zipf's law in the corpus"
author: "Niko Ilomäki"
date: "Thursday, May 14, 2015"
output: markdown_document
---



# What about Zipf's law?

![plot of chunk zipf](figure/zipf-1.png) 


```r
fit <- power.law.fit(frequencies,xmin=947)
fit$KS.p
```

```
## [1] 0.995389
```
