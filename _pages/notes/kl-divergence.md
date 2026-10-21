---
layout: page
title: "KL Divergence and Modern Statistics"
permalink: /reading/kl-divergence/
nav: false
math: true
toc:
  sidebar: left
---

[← Reading]({{ '/reading/' | relative_url }})

# Modern Statistics

Loss function is a "scanning apparatus". It will take special value at the true parameter such as 0 or minimum point.





##  Empirical Kullback-Leibler Divergence Loss and MLE

(Empirical loss means that since we do not know the true distribution, we could use the sample to approximate the loss function.
)

Consider the empirical loss function：

$$l(\theta) = \mathbb{E}_{\Theta} \left[ \frac{f(x;\theta_0)}{f(x;\theta)} \log \frac{f(x;\theta_0)}{f(x;\theta)} \right]$$

$$= \int \frac{f(x;\theta_0)}{f(x;\theta)} \log \frac{f(x;\theta_0)}{f(x;\theta)} f(x;\theta) dx$$

$$= \int \left[ \log \frac{f(x;\theta_0)}{f(x;\theta)} \right] f(x;\theta_0) dx$$

$$= \mathbb{E}_{\Theta_0} \left[ \log \frac{f(x;\theta_0)}{f(x;\theta)} \right]$$

$$\approx \frac{1}{n} \sum_{i=1}^{n} \log \frac{f(x_i;\theta_0)}{f(x_i;\theta)}$$

$$= \frac{1}{n} \sum_{i=1}^{n} \log f(x_i;\theta_0) - \frac{1}{n} \sum_{i=1}^{n} \log f(x_i;\theta)$$



$$\text{Argmin}(\hat{\theta}) = \text{Argmin}\left[ -\frac{1}{n} \sum_{i=1}^{n} \log f(x_i;\theta) \right]$$

$$= \text{Argmax}\left[ \sum_{i=1}^{n} \log f(x_i;\theta) \right]$$

$$= \text{Argmax}\left[ \log \prod_{i=1}^{n} f(x_i;\theta) \right]$$

### KL-divergence Property

Let $E_{\theta}$ be the expectation of $f_{\theta}(x)$.

the true model  $f(x;\theta_0)$，and the proposed model is $f(x,\theta)$。

KL (entropy) divergence:

$$\mathbb{E}_{\theta} \left[ \frac{f(x;\theta_0)}{f(x;\theta)} \log \frac{f(x;\theta_0)}{f(x;\theta)} \right]$$

Let $\varphi(x) = x \log x$，then $\varphi'(x) = \log x + 1$，$\varphi''(x) = \frac{1}{x} > 0$，  

So $\varphi(x)$  is a convex function over $(0,+\infty)$.。

By Jensen inequality：

$$\varphi\left( \mathbb{E}_{\theta} \left[ \frac{f(x;\theta_0)}{f(x;\theta)} \right] \right) \leq \mathbb{E}_{\theta} \left[ \varphi\left( \frac{f(x;\theta_0)}{f(x;\theta)} \right) \right]$$



$$\mathbb{E}_{\theta} \left[ \frac{f(x;\theta_0)}{f(x;\theta)} \right] = \int_{-\infty}^{\infty} \frac{f(x;\theta_0)}{f(x;\theta)} f(x;\theta) dx$$

$$= \int_{-\infty}^{\infty} f(x;\theta_0) dx = 1$$

Thus

$$\varphi(1) = 1 \times \log 1 = 0 \leq \mathbb{E}_{\theta} \left[ \frac{f(x;\theta_0)}{f(x;\theta)} \log \frac{f(x;\theta_0)}{f(x;\theta)} \right]$$

Loss function

$$l(\theta) = \mathbb{E}_{\theta} \left[ \frac{f(x;\theta_0)}{f(x;\theta)} \log \frac{f(x;\theta_0)}{f(x;\theta)} \right] \geq 0$$

and $l(\theta_0) = 0$，so $\theta_0$ is $l(\theta)$'s minimum point

Empirical estimators are:

$$l(\theta) \approx \frac{1}{n} \sum_{i=1}^n \frac{f(x_i;\theta_0)}{f(x_i;\theta)} \log \frac{f(x_i;\theta_0)}{f(x_i;\theta)}$$


**Conclusion: Maximum likelihood estimation is equivalent to minimizing the KL divergence, which provides the theoretical basis of information theory for MLE. **




DeepSeek loss function---Feed the data - gradient descent---LLM






statistical distribution

distribution function used to examine the question, like Laplace's error function but much more complicated, using probability theory to describe what might be expected from future data taken at random from the same population of people
