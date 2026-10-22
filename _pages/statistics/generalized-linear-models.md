---
layout: page
title: "Generalized Linear Models"
permalink: /statistics/generalized-linear-models/
nav: false
lecture_note: true
math: true
toc:
  sidebar: left
---

[← Lecture Notes]({{ '/math/' | relative_url }})

{% raw %}
# MTH303: Linear Statistical Models

Thanks to Dr. Mu He for instructing us in core linear model concepts and sharing compelling stories and history of statistics. This has greatly deepened my appreciation for the elegance of statistics embodied in four decades of traditional linear models, as well as what constitutes thoughtful statistical judgment and taste for inference in the modern computing era.

The notes below bring together the course's regression, inference, categorical-predictor, likelihood, and generalized linear model ideas. Throughout, $n$ is the number of observations; $p$ counts slopes, so a design matrix with an intercept has $p+1$ columns.

## From a mean to a regression model

A sample mean predicts every observation in the same way. It is useful when observations can reasonably be treated as exchangeable around one common mean. If a measured covariate explains systematic differences, a conditional mean is more informative: $m(x)=E(Y\mid X=x)$. In simple linear regression (SLR), we approximate this mean by $\beta_0+\beta_1x$. The line is a model for the *mean*, while the random error describes variation around it:

$$Y_i=\beta_0+\beta_1x_i+\varepsilon_i,\qquad E(\varepsilon_i\mid X)=0,\qquad \operatorname{Var}(\varepsilon_i\mid X)=\sigma^2.$$

For the classical normal theory used below, condition additionally on the design and assume $\varepsilon\sim N_n(0,\sigma^2I_n)$. Least squares itself does not require normality; the exact small-sample $t$ and $F$ distributions do. A slope is the change in the modeled mean per unit change in $x$. With several predictors, its interpretation is conditional on the other predictors being held fixed. An intercept describes the modeled mean when the included predictors are zero, which need not be a scientifically meaningful setting.

### Least squares, fitted values, and residuals

The least-squares line minimizes $\operatorname{RSS}(b_0,b_1)=\sum_i(y_i-b_0-b_1x_i)^2$. Writing $S_{xx}=\sum_i(x_i-\bar x)^2$ and $S_{xy}=\sum_i(x_i-\bar x)(y_i-\bar y)$ gives

$$\hat\beta_1=\frac{S_{xy}}{S_{xx}},\qquad \hat\beta_0=\bar y-\hat\beta_1\bar x,\qquad \hat y_i=\hat\beta_0+\hat\beta_1x_i,\qquad e_i=y_i-\hat y_i.$$

The fitted line passes through $(\bar x,\bar y)$. Residuals are observed differences from that fitted line; they are not the unobserved errors $\varepsilon_i$. With an intercept, the normal equations imply $\sum_i e_i=0$ and $\sum_i x_ie_i=0$. Geometrically, $\hat y$ is the orthogonal projection of the response vector $y$ onto the column space of the design matrix, and $e$ is perpendicular to that space. This geometry explains the normal equations without claiming that the realized $y$ must lie on the fitted line.

### Variation and the ANOVA comparison

With an intercept, $y_i-\bar y=(\hat y_i-\bar y)+e_i$, and the two terms are orthogonal. Therefore

$$\underbrace{\sum_i(y_i-\bar y)^2}_{\mathrm{TSS}}=\underbrace{\sum_i(\hat y_i-\bar y)^2}_{\mathrm{RegSS}}+\underbrace{\sum_i e_i^2}_{\mathrm{RSS}},\qquad R^2=1-\frac{\mathrm{RSS}}{\mathrm{TSS}}.$$

TSS has $n-1$ degrees of freedom. For SLR, RegSS has one and RSS has $n-2$; for full-rank multiple regression with $p$ slopes, these become $p$ and $n-p-1$. The residual mean square $s^2=\mathrm{RSS}/(n-p-1)$ estimates $\sigma^2$ under the model. The global statistic

$$F=\frac{\mathrm{RegSS}/p}{\mathrm{RSS}/(n-p-1)}$$

tests whether all slopes are zero. A large $F$ is evidence that the predictors explain variation beyond an intercept-only model. $R^2$ describes the fraction of sample variation explained relative to that baseline; it does not by itself establish causality or whether the assumptions are adequate. In SLR, the two-sided slope $t$ test and the global $F$ test agree because $F=t^2$.

### Uncertainty for a coefficient and for a future response

Under the normal SLR assumptions, $\hat\beta_1\sim N(\beta_1,\sigma^2/S_{xx})$, so a $t$ statistic replaces $\sigma$ with $s$. A two-sided confidence interval is $\hat\beta_1\pm t_{n-2,1-\alpha/2}s/\sqrt{S_{xx}}$. The slope test asks about the conditional mean; predicting a new individual response also requires accounting for a new error term.

At a chosen $x_*$, $\hat m(x_*)=\hat\beta_0+\hat\beta_1x_*$. Its estimated standard error is $s\sqrt{1/n+(x_*-\bar x)^2/S_{xx}}$, whereas the predictive standard error for a future $Y_*$ is

$$s\sqrt{1+\frac1n+\frac{(x_*-\bar x)^2}{S_{xx}}}.$$

Thus a prediction interval uses $\hat m(x_*)\pm t_{n-2,1-\alpha/2}$ times the second standard error. It is wider than the corresponding interval for the mean because it includes the future observation's intrinsic variation.

## Multiple regression as a projection

For $p$ slopes, write $y=X\beta+\varepsilon$, where $X$ is $n\times(p+1)$ and includes a column of ones. If $X$ has full column rank, least squares gives

$$\hat\beta=(X^TX)^{-1}X^Ty,\qquad H=X(X^TX)^{-1}X^T,\qquad \hat y=Hy,\qquad e=(I-H)y.$$

$H$ is the *hat matrix*: $H^T=H$ and $H^2=H$. It projects onto $\operatorname{col}(X)$, while $M=I-H$ projects onto its orthogonal complement. Hence $X^Te=0$, $\hat y^Te=0$, and a full-rank model leaves $n-p-1$ residual degrees of freedom. An interaction term, such as $x_1x_2$, allows the slope of one continuous predictor to depend on the other; with a binary $z$, $\beta_0+\beta_1x+\beta_2z+\beta_3xz$ gives an intercept change $\beta_2$ and a slope change $\beta_3$ between groups.

Under $\varepsilon\sim N_n(0,\sigma^2I)$ conditional on $X$,

$$\hat\beta\mid X\sim N_{p+1}\!\left(\beta,\sigma^2(X^TX)^{-1}\right),\quad e\mid X\sim N_n(0,\sigma^2M),\quad \frac{\mathrm{RSS}}{\sigma^2}=\frac{e^Te}{\sigma^2}\sim\chi^2_{n-p-1}.$$

The last result follows because $M$ is symmetric and idempotent with rank $n-p-1$: in a suitable orthonormal basis, its quadratic form is the sum of that many squared independent standard normals. Moreover,

$$\operatorname{Cov}(e,\hat\beta\mid X)=\sigma^2M X(X^TX)^{-1}=0.$$

Both are linear transformations of a jointly normal vector, so zero covariance makes $e$ and $\hat\beta$ independent. The same is true of $e$ and $\hat y$. Under the intercept-only null, $\mathrm{RegSS}/\sigma^2\sim\chi^2_p$, independently of $\mathrm{RSS}/\sigma^2$, which leads to the global $F$ test above. These exact independence statements use the normal-error model; orthogonality of fitted values and residuals alone is a geometric fact.

### Single and grouped questions

A single coefficient can be tested with $t=(\hat\beta_j-\beta_{j,0})/[s\sqrt{(X^TX)^{-1}_{jj}}]$, using $n-p-1$ degrees of freedom. For a group of $q$ coefficients, fit a *reduced* model under the restriction and a *full* model containing the additional terms. Then

$$F=\frac{(\mathrm{RSS}_{R}-\mathrm{RSS}_{F})/q}{\mathrm{RSS}_{F}/(n-p-1)}\sim F_{q,n-p-1}\quad\text{under }H_0.$$

This partial $F$ test asks whether the group improves fit after the other variables have been included. It is more appropriate for a joint hypothesis than choosing among several individual $t$ tests. The models must be nested, and both RSS values must be computed from the same responses.

## Categorical predictors: a change of coordinates

A categorical predictor with $r$ levels needs $r-1$ independent columns when the model has an intercept. Including all $r$ indicators as well as the intercept makes $X$ rank deficient, because the indicators sum to the intercept column. With treatment coding, the omitted level is a reference group, and each displayed coefficient is a difference from its mean. With effect coding, coefficients describe deviations under the chosen sum-to-zero constraint. The numerical coefficients and their interpretation change with the coding, while the fitted group means need not.

The tutorial's education example has three levels: no high school, completed high school, and post-secondary. Its effect-coded rows for $(1,E,F)$ are $(1,1,0)$, $(1,0,1)$, and $(1,-1,-1)$. Treatment coding with post-secondary as reference instead uses $(1,D_N,D_C)$ with rows $(1,1,0)$, $(1,0,1)$, and $(1,0,0)$. For the same three observations these design matrices satisfy $X_{\mathrm{effect}}=X_{\mathrm{dummy}}T$, where

$$T=\begin{pmatrix}1&-1&-1\\0&2&1\\0&1&2\end{pmatrix},\qquad \det(T)=3\ne0.$$

Thus $\operatorname{col}(X_{\mathrm{effect}})=\operatorname{col}(X_{\mathrm{dummy}})$. More generally, any invertible column change $X_2=X_1T$ gives $\beta_2=T^{-1}\beta_1$, the same fitted values, and the same projection matrix $H_2=H_1$. This is *matrix reparameterization*: an individual coefficient may look different, but a properly translated contrast and its inference describe the same group comparison. For two categorical factors, both parameterizations must also represent the same intended main effects and interactions before their fits can be compared.

In the tutorial's additive wage example, education uses $(E,F)$ and number of children uses $(G,H)$, each with three levels. The mean for post-secondary education and more than two children is $a-b_1-b_2-c_1-c_2$ under the stated effect coding. Its contrast with the balanced average of all nine education-by-children cell means is $-b_1-b_2-c_1-c_2$. A sample-weighted average is a different target when group sizes are unequal; the reference average must be specified before interpreting a contrast.

## Likelihood and maximum likelihood estimation

For independent observations with density or mass $f(y_i;\theta)$, the likelihood is $L(\theta;y)=\prod_i f(y_i;\theta)$ and the log-likelihood is $\ell(\theta;y)=\sum_i\log f(y_i;\theta)$. The data are fixed in this optimization; $\theta$ varies. Maximizing $L$ or $\ell$ gives the same estimate. A zero derivative identifies a candidate stationary point, not automatically a global maximum or a boundary solution.

For Bernoulli responses, the MLE of their common success probability is the sample proportion. For independent exponential observations parameterized by rate $\lambda$, $\hat\lambda=1/\bar y$. Under a normal model, the likelihood estimators are $\hat\mu=\bar y$ and $\hat\sigma^2_{\mathrm{MLE}}=n^{-1}\sum_i(y_i-\bar y)^2$; the unbiased sample variance uses $n-1$ instead. This distinction also appears in normal regression: the MLE of $\sigma^2$ divides RSS by $n$, while the usual residual mean square divides by the residual degrees of freedom.

## Generalized linear models

A GLM keeps a linear *predictor* $\eta_i=x_i^T\beta$ while allowing the response distribution and mean-to-predictor relationship to change. It has three parts:

1. A random component: conditionally independent $Y_i$ from a specified exponential dispersion family.
2. A systematic component: $\eta_i=x_i^T\beta$.
3. A link: $g(\mu_i)=\eta_i$, where $\mu_i=E(Y_i\mid x_i)$.

A positive-valued outcome illustrates why this matters. Fitting a straight line on the original scale can predict negative means. Regressing $\log Y$ changes the modeled response and targets $E(\log Y\mid x)$, which is not generally $\log E(Y\mid x)$. A GLM with a log link instead specifies $\log E(Y\mid x)=x^T\beta$ directly, with an appropriate response family and variance. This distinction is important even when both approaches can produce visually straight plots after a transformation.

### Exponential family, mean, and variance

Write an exponential dispersion family as

$$f(y;\theta,\phi)=\exp\left\{\frac{y\theta-b(\theta)}{a(\phi)}+c(y,\phi)\right\}.$$

Here $\theta$ is the natural parameter and $\phi$ controls dispersion. Differentiating the normalized density and using the expected score equal to zero gives $\mu=b'(\theta)$. Differentiating again gives $\operatorname{Var}(Y)=a(\phi)b''(\theta)$. The *variance function* is $V(\mu)=b''(\theta(\mu))$, so $\operatorname{Var}(Y)=a(\phi)V(\mu)$. The link is *canonical* when $g(\mu)=\theta(\mu)$.

| Response family | Mean $\mu$ | Variance function $V(\mu)$ | Common link |
| --- | --- | --- | --- |
| Gaussian | $\mu$ | $1$ | Identity |
| Bernoulli | $\mu$ | $\mu(1-\mu)$ | Logit |
| Poisson | $\mu$ | $\mu$ | Log |
| Gamma | $\mu$ | $\mu^2$ | Inverse (up to parameterization) |
| Inverse Gaussian | $\mu$ | $\mu^3$ | Inverse-squared (up to scale) |

The mean-variance relationship is part of the model, not merely a nuisance. For Bernoulli outcomes, the variance depends on the mean even when observations are otherwise independent. The canonical parameterization is not the only possible parameterization, and a valid GLM need not use its canonical link.

### Links and interpretations

With a Gaussian response and identity link, $\mu_i=x_i^T\beta$ recovers ordinary normal linear regression. For Poisson counts, $\log\mu_i=x_i^T\beta$ guarantees $\mu_i>0$ and gives $\mu_i=\exp(x_i^T\beta)$; a one-unit change in a predictor multiplies the modeled mean by $e^{\beta_j}$ when other predictors are held fixed. For binary outcomes, the logistic model uses

$$\log\frac{\pi_i}{1-\pi_i}=x_i^T\beta,\qquad \pi_i=\frac{e^{x_i^T\beta}}{1+e^{x_i^T\beta}},$$

so $e^{\beta_j}$ is a conditional odds ratio for a one-unit change. The probit alternative uses $\Phi^{-1}(\pi_i)=x_i^T\beta$ and therefore $\pi_i=\Phi(x_i^T\beta)$. Both keep fitted probabilities between zero and one; their coefficient scales differ.

### Score equations and a working response

Let $g(\mu_i)=\eta_i=x_i^T\beta$ and $\theta_i=\theta(\mu_i)$. Applying the chain rule to the log-likelihood gives the score component

$$U_j(\beta)=\sum_{i=1}^n\frac{(y_i-\mu_i)x_{ij}}{a(\phi)V(\mu_i)g'(\mu_i)}.$$

Define $w_i=1/[V(\mu_i)\{g'(\mu_i)\}^2]$ and the local working response $z_i=\eta_i+g'(\mu_i)(y_i-\mu_i)$. Then

$$U(\beta)=\frac{1}{a(\phi)}X^TW(z-X\beta),\qquad W=\operatorname{diag}(w_1,\ldots,w_n).$$

These weights and responses depend on the current $\beta$; solving $X^TWX\beta=X^TWz$ therefore means updating them iteratively, rather than performing one ordinary least-squares fit. Locally, $z_i$ linearizes the link around the current fitted mean, and $w_i$ reflects its variance. For normal errors with an identity link, $w_i=1$ and $z_i=y_i$, reproducing $X^T(y-X\beta)=0$. For a Poisson log-link model, $V(\mu_i)=\mu_i$, $g'(\mu_i)=1/\mu_i$, hence $w_i=\mu_i$ and $z_i=\eta_i+(y_i-\mu_i)/\mu_i$; the score reduces to $X^T(y-\mu)=0$.

The practical lesson across all these models is to choose the response distribution, link, predictor coding, and inferential target together. A familiar coefficient or small $p$-value is only useful after its model and comparison have been made explicit.

---
{% endraw %}

{% raw %}
# Linear Regression

## Partial modeling--P(x\|y)

For many points, there are many possible regression functions f (nonparametric) so it is useful to restrict to simple functions described by a few parameters.

Though true regression functions are never linear, we assume the dependence of Y on $X_1$...$X_n$ is linear.

regression function: x----\> f(x) : $$ E[Y|X=x]= \int yh(y|x)dy$$ (ps: the conditional median:m(x) $$\int_{-\infty}^{m(x)}\ h(y|x)dy=1/2$$)

## Simple linear regression

-   **OLS(Ordinary Least-Squares)**: Historically, the OLS method was introduced before the systematic understanding of conditional expectation. The OLS method was proposed by French mathematician Adrien-Marie Legendre in 1805 and later developed by Carl Friedrich Gauss in 1809. The OLS method was created to find the regression coefficients that best fit the data. An interesting geometry explaination in Linear Algebra's projection matrix of OLS in multiple(simple) linear regression:

-   **Conditional Expectation**: After the OLS method was established, it was recognized that the regression equation obtained through OLS is actually the expected value of (Y) given (X), i.e., the conditional expectation (E(Y\|X=x)). Under the classical linear regression assumptions, the OLS estimate is an unbiased estimate of the conditional expectation.

Specifically, for a simple linear regression model ($$Y = \beta_0 + \beta_1X + \epsilon$$):

-   **OLS Estimate**: Through the OLS method, we obtain the estimated regression coefficients ($\hat{\beta}_0$) and ($\hat{\beta}_1$), thus writing the regression equation ($$\hat{Y} = \hat{\beta}_0 + \hat{\beta}_1X$$). (based on the smallest RSS)

-   **Conditional Expectation**: According to the model assumption, the conditional expectation (E(Y\|X=x)) should be ($\beta_0 + \beta_1x$)(which is called the real regression line(not the true line) and could not be seen in practice). The regression equation obtained through OLS, ($\hat{Y} = \hat{\beta}_0 + \hat{\beta}_1X$), is an estimate of (E(Y\|X=x)).

In summary, OLS(similar to MLE in SLR) is the best way to estimate the true model, which generates the unbiased estimators of the real regression line that based on $E[y_i|x]$.

### Another explaination--analogy of population mean in sampling distribution:

### essence of SLR relavant to ρ (correlation coefficient)

$$\hat{y}-\bar{y}/sd(\hat{y})=\rho(\hat{x}-\bar{x}/sd(\hat{x}))$$

#### Proof using covariance when it is normal distribution(Teacher:shisong mao)

### Hypothesis test in (simple/multiple--the same philosophy) Linear Regression

#### t-statistics for estimators

z----t----F

##### slope

$H_0$:$\beta_1$=0 \###### t for testing significance of regression Because $y_i=\hat{\beta}_0+\hat{\beta}_1 x_i$\~NID($\beta_0+\beta_1x_i,\sigma^2$), $\beta_1$\~N($\beta_1$,$\sigma^2\Sigma (x_i-\bar{x})^2$ so if $\sigma$ is known, $$\hat{\beta}_1/ \sqrt {\sigma^2/\Sigma (x_i-\bar{x})^2}$$ but if $\sigma$ is unknown, $$t_0=\hat{\beta}_1/se( \hat{\beta}_1)$$, which just substitute $\sigma$'s unbiased estimation($\Sigma (y_i-\hat{y})^2/n-2$, which is RSS)for $\sigma$.

###### F of analysis of variance for testing the significance of regression(2 ways to understand F test—model interpretation and hypothesis test with noncentralirity parameter(0 or not 0)

$$\frac{\Sigma (y_i-\hat{y})^2}{\sigma^2p}/\frac{\Sigma(\hat{y}-\bar{y})^2}{\sigma^2(n-p-1)} \sim F$$

The F-statistic essentially compares the amount of systematic variance explained by the model to the amount of unsystematic variance (error) and helps determine the overall significance of the model. This is why the equation can express the model's explanatory power andrelationship with hypothesis testing.

If $H_0$ is true, F is a centrality parameter. If we reject $H_0$, F follows 1 and n-2 degrees of freedom for simple linear regression and a noncentrality parameter is $$\lambda=\beta_1^2\frac{\Sigma(x_i-\bar{x})^2}{\sigma^2}$$ and $\lambda$ is not = 0. Also, F represents the ability of model's explanation, so if F$>1$, or $>$ the certain threshold, the model is good.

As for one variable's test, t is more adaptable because of its one-sided alternative hypotheses although it is equivalent to the F test for the simple linear regression.

###### the statistical properties of the maximum-likelihood estimators(2.10)

# Logistic regression

Instead of linear OLS regression we use something called logistic regression, which is probably more widely used (especially if include variants) than linear OLS. \## why not SLR? (1)SLR may predict values that are below zero or above 1 (2)For SLR we assumed that the population distribution was normally distributed around the mean, for each value of the X variable. That’s not going to be the case if we’ve got a binary response.

### Test the model

ML-LRT-compare the maximum of the likelihood function for each model

#### cross validation
###r example of logistic regression with variable selection and model selection
####Check the goodness of fit----Hosmer-Lemeshow GOF test is the most widely used for logistic regression model.
### r example

```r
require(ISLR)
library(ISLR2)
names(Smarket)
dim(Smarket)
summary(Smarket)
pairs(Smarket)
###

cor(Smarket[, -9])
###
attach(Smarket)
plot(Volume)

## Logistic Regression

###
glm.fits <- glm(
  Direction ~ Lag1 + Lag2 + Lag3 + Lag4 + Lag5 + Volume,
  data = Smarket, family = binomial
)
##family=binomial tells R to use logistic regression????mary(glm.fits)
###
coef(glm.fits)
summary(glm.fits)
# Null deviance: deviance for just mean(if you only use mean model it is log likelihood
#Residual deviance: deviance for the model with all the predictors in 
#(e.g. 1731,1249 df;1727,1243 df)
#? r上的glm对于binary就是logistic？
#? LDA的coefficient是怎么生成的（原理）（by hand e.g.)
summary(glm.fits)$coef
summary(glm.fits)$coef[, 4]
###
glm.probs <- predict(glm.fits, type = "response")#response variable, as opposite to omitting or type=link
glm.probs[1:10]
contrasts(Direction)
###

glm.pred <- rep("Down", 1250)
glm.pred[glm.probs > .5] = "Up"
```
<figure class="note-figure" style="max-width:560px;margin:1.3rem auto;"><img src="/assets/img/code-output/glm-pre-qmd/chunk-001-1.png" alt="Output from code example 1" loading="lazy" style="display:block;max-width:100%;max-height:420px;width:auto;height:auto;margin:auto;object-fit:contain;"><figcaption style="font-size:.88rem;color:#666;text-align:center;margin-top:.45rem;">Output from code example 1</figcaption></figure>
<figure class="note-figure" style="max-width:560px;margin:1.3rem auto;"><img src="/assets/img/code-output/glm-pre-qmd/chunk-001-2.png" alt="Output from code example 1" loading="lazy" style="display:block;max-width:100%;max-height:420px;width:auto;height:auto;margin:auto;object-fit:contain;"><figcaption style="font-size:.88rem;color:#666;text-align:center;margin-top:.45rem;">Output from code example 1</figcaption></figure>
{% endraw %}
