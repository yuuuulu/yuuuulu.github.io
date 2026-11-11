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

# Estimation

Let $X_1,\ldots,X_n$ be independent observations from a model $f(x;\theta)$, where $\theta$ is unknown. Different estimators use different summaries of the data or different criteria for choosing $\theta$.

## Method of moments

Match theoretical moments to sample moments. For $k$ parameters, solve $k$ equations:

$$
m_j(\theta)=\mathbb E_\theta[X^j],\qquad
\widehat m_j=\frac1n\sum_{i=1}^n X_i^j,\qquad
m_j(\widehat\theta_{\mathrm{MoM}})=\widehat m_j,\qquad j=1,\ldots,k.
$$

For one parameter, if $m_1$ is invertible,

$$
\widehat\theta_{\mathrm{MoM}}=m_1^{-1}(\overline X).
$$

The law of large numbers explains why $\widehat m_j$ approaches $m_j(\theta)$ when the relevant moment exists. Computing the theoretical moments still requires a specified model.

## Bayesian estimation

A prior $\pi(\theta)$ and the likelihood $L(\theta;x)$ give the posterior density

$$
L(\theta;x)=\prod_{i=1}^n f(x_i;\theta),\qquad
\pi(\theta\mid x)=
\frac{L(\theta;x)\pi(\theta)}
{\int_\Theta L(t;x)\pi(t)\,dt}.
$$

The posterior updates prior assumptions with observed data. Common summaries include

$$
\widehat\theta_{\mathrm{mean}}=\mathbb E[\theta\mid x],\qquad
\widehat\theta_{\mathrm{MAP}}=\operatorname*{arg\,max}_{\theta\in\Theta}\pi(\theta\mid x).
$$

A posterior credible interval is another summary. More generally, a Bayesian action $a$ minimizes posterior expected loss:

$$
\widehat a=\operatorname*{arg\,min}_{a}\mathbb E[\ell(a,\theta)\mid x].
$$

For squared-error loss, this action is the posterior mean; for absolute-error loss, a posterior median.

## Fisher, likelihood, and MLE

Maximum likelihood uses the sampling model directly, without assigning a prior probability to $\theta$:

$$
\widehat\theta_{\mathrm{MLE}}
=\operatorname*{arg\,max}_{\theta\in\Theta}L(\theta;x)
=\operatorname*{arg\,max}_{\theta\in\Theta}\ell(\theta;x),
\qquad
\ell(\theta;x)=\sum_{i=1}^n\log f(x_i;\theta).
$$

For an interior optimum, a candidate solves the score equation $\partial\ell(\theta;x)/\partial\theta=0$; boundaries and other stationary points must also be checked.

Fisher's early argument used *inverse probability*. In his [1922 account of theoretical statistics](https://digital.library.adelaide.edu.au/items/36b96da4-e256-4e94-9720-eef372935c3a), he acknowledged that starting point and then distinguished **likelihood** from a probability distribution over parameter values. His mature MLE therefore does not depend on choosing a uniform prior.

### When does a uniform prior give the same estimate?

If $\Theta=[a,b]$ and $\pi(\theta)=1/(b-a)$ on $\Theta$, with a finite positive normalizing integral, then

$$
\pi(\theta\mid x)
=\frac{L(\theta;x)}{\int_a^b L(t;x)\,dt}
\propto L(\theta;x),\qquad \theta\in[a,b].
$$

Hence, when the maxima exist,

$$
\boxed{\widehat\theta_{\mathrm{MAP}}
=\operatorname*{arg\,max}_{\theta\in[a,b]}L(\theta;x)
=\widehat\theta_{\mathrm{MLE},[a,b]}.}
$$

This is an equality of *optimizers on the same parameter space*, not an equality between posterior density and likelihood. It does not turn Fisher's MLE into a Bayesian method.

A flat prior also depends on the parameterization. For $\phi=e^\theta$,

$$
\pi_\phi(\phi)
=\pi_\theta(\log\phi)\left|\frac{d\log\phi}{d\phi}\right|
=\frac{1}{(b-a)\phi},\qquad e^a\leq\phi\leq e^b.
$$

Thus a prior uniform in $\theta$ is not uniform in $\phi$. The MLE transforms as $\widehat\phi_{\mathrm{MLE}}=e^{\widehat\theta_{\mathrm{MLE}}}$, whereas posterior density modes generally depend on the chosen parameterization.
