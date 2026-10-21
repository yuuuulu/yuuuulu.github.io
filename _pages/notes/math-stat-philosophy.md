---
layout: page
title: Philosophy and Math/Stat
permalink: /reading/math-stat-philosophy/
nav: false
math: true
---

[← Reading]({{ '/reading/' | relative_url }})

## Geometry from iteration

The volume of an $n$-dimensional ball becomes manageable when I slice it into lower-dimensional balls. Integrating two coordinates gives the recurrence $V_n(1)=\frac{2\pi}{n}V_{n-2}(1)$; with $V_0(1)=1$ and $V_1(1)=2$, it leads to $V_n(R)=\frac{\pi^{n/2}R^n}{\Gamma(n/2+1)}$. A high-dimensional integral can emerge from repeated ordinary integrals. This is why the derivation stays with me. See [Calculus]({{ '/math/calculus/' | relative_url }}).

## Examples before abstraction

A diagram of an approximating sequence may suggest a limit before I can prove it. A counterexample tests the exact reach of a theorem. The proof then explains why the intuition works and where it stops. See [Analysis 1]({{ '/math/analysis-1/' | relative_url }}).

## Models are approximations

Differential equations describe change with explicit assumptions; statistical models describe uncertainty with theirs. Neither is nature itself. A useful model has to be checked against the phenomenon and the data. See [Differential Equations]({{ '/math/differential-equations/' | relative_url }}) and [Statistical Learning]({{ '/math/statistical-learning/' | relative_url }}).

## Projection and inference

A least-squares projection separates a fitted component from a residual. That simple geometric picture connects linear algebra with regression, while reminding me that unexplained variation remains. See [Advanced Linear Algebra]({{ '/math/linear-algebra/' | relative_url }}) and [Generalized Linear Models]({{ '/statistics/generalized-linear-models/' | relative_url }}).

## 从例子走向证明 · From examples to proof

例子和反例帮助我看清定理的适用范围；证明则解释其中的逻辑。Examples and counterexamples show where a theorem applies; proof explains why.
