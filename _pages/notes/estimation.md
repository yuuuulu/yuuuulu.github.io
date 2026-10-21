---
layout: page
title: "Estimation"
permalink: /reading/estimation/
nav: false
math: true
toc:
  sidebar: left
---

[← Reading]({{ '/reading/' | relative_url }})

# statistics

population $f(x;\theta)$ and $\theta$ is unknown


## old/classical: Bayesian estimation; moment estimation

## Moment estimation

- For the moment estimation, we do not know the density so we could not calculate the expectation directly. Instead, we use LLN to approximate the expectation with sample mean. We then have

$$
m_1(\theta) = E[X] \approx \bar{X} = \frac{1}{n} \sum_{i=1}^n X_i
$$

then
$$
\hat \theta = m_1^{-1}(\frac{1}{n} \sum_{i=1}^n X_i)
$$

For the multiple parameter case, we could use multiple moments to estimate the parameters. (k equations to solve k unknown parameters). Here we do not know the precise distribution, so we could not calculate the moments directly. Instead, we use LLN to approximate the moments with sample moments. 

Suppose $X_1, X_2, \ldots, X_n$ are iid samples from the distribution with parameters $f(x;\theta_1, \theta_2, \ldots, \theta_k)$ then by LLM. 

We then have approximatedmoment equation:

$$
E[X^j] = m_j(\theta_1, \theta_2, \ldots, \theta_k) \approx \frac{1}{n} \sum_{i=1}^n X_i^j, j=1,2,\ldots,k
$$

then we could solve the equations to get the estimators.

The solution $\hat \theta_1, \hat \theta_2, \ldots, \hat \theta_k$ are the moment estimators of the parameters.

## Bayesian estimation

$f(x|\theta)$ is regarded as conditional density and the unknown parameter $\theta$ is the condition. $\theta$ is a random variable with prior distribution $\pi(\theta)$.

$(X, \theta)$ has joint distribution $f(x,\theta)=f(x|\theta)\pi(\theta)$

Then we get the marginal distribution of $X$:

$f_X(x) = \int_{-\infty}^{+\infty} f(x|\theta)\pi(\theta)d\theta=\int_{-\infty}^{+\infty} f(x;\theta)\pi(\theta)d\theta$


the Bayesian formula is 

$$ \frac {P(A|C_i)P(C_i)}{\sum_j P(A|C_j)P(C_j)} =P(C_i|A)$$


$$
f(\theta|x)=\frac{f(x|\theta)\pi(\theta)}{f_X(x)} = \frac{f(x;\theta)\pi(\theta)}{\int_{-\infty}^{+\infty} f(x;\theta)\pi(\theta)d\theta}
$$

Then above we have used Bayes theorem to get the posterior distribution of $\theta$ given $X=x$

This is the updation of your belief or learning.

Bayesian statistics is unclear and ambiguous, but leaving us with no choice but to incorporate the most fundamental knowledge we have （不清不楚，不得不用）. We then update our understanding through experimental data. If it cannot be accomplished in one attempt, we iterate multiple times—eventually, we will gain a solid understanding of the parameters. The learning process is one of repeated iteration; there is no need to expect it to be completed in a single attempt.

When we do not know every knowledge about the model, we could use the prior of uniform distribution to represent our ignorance. That is, everyone is equally likely.


for $f(x;\theta)$, we could calculate the expectation ; mode; CI

modern statistics

$L(\theta) = E[R(\theta,X)]$

$\hat \theta = argmin_\theta L(\theta)$

where $R(\theta,X)$ is the loss function

## Fisher: MLE

**Fisher ambitious ： 不想依赖于贝叶斯，选prior的时候不能包含个人的任何认知，那就选客观的uniform分布**
(Fisher ambitious: Not wanting to rely on Bayesian, when choosing prior, no personal cognition can be included. Then choose the objective uniform distribution)

$\pi (\theta|x) {d\theta}= d\theta$ uniform

$f(\theta|x_1, x_2, \ldots, x_n) = \frac{f(x_1, x_2, \ldots, x_n;\theta)\pi(\theta)}{\int f(x_1, x_2, \ldots, x_n;\theta)\pi(\theta)d\theta}$ = $L(\theta)$

$$
= \frac{f(x_1;\theta)f(x_2;\theta)\ldots f(x_n;\theta) }{\int f(x_1;\theta)f(x_2;\theta)\ldots f(x_n;\theta)  d\theta}=L(\theta)
$$

Mode:

Find maximum of $f(\theta|x_1, x_2, \ldots, x_n)$ i.e. L($\theta$)

$\hat \theta = argmax_\theta L(\theta)=argmax_\theta \frac{f(x_1;\theta)f(x_2;\theta)\ldots f(x_n;\theta)}{f_X(x_1,x_2,..x_n)}$

$= argmax_\theta f(x_1;\theta)f(x_2;\theta)\ldots f(x_n;\theta)=argmax_\theta L(\theta)$ this is the likelihood function



When Fisher wanted to publish his idea to the Royal Society, he had been harshly commented through the discussion of the Royal Society. This is a good tradition but nowadays' conference does ntot keep this. This means now they just have a presentation but the comments will not appear in the published paper.



then we could use log likelihood to simplify the calculation of the derivative to get the maximum likelihood estimator.





modern: Loss function
