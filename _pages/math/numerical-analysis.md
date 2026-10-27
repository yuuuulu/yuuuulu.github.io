---
layout: page
title: "Numerical Analysis"
permalink: /math/numerical-analysis/
nav: false
lecture_note: true
math: true
toc:
  sidebar: left
---

[← Lecture Notes]({{ '/math/' | relative_url }})

{% raw %}
# MTH208 Numerical Analysis: key ideas

These concise notes follow Lectures 1–13 and the additional cubic-spline slides. The main questions are how to approximate a mathematical object, how errors enter the computation, and whether the chosen algorithm preserves the useful information in the data.

## Lecture 1 — floating-point arithmetic and error

- A computer stores a finite set of floating-point numbers. Chopping discards extra digits; rounding chooses the nearest representable value. Neither makes real arithmetic exact.
- **Absolute error** is $|x-\hat x|$; **relative error** is $|x-\hat x|/|x|$ when $x\ne0$. Relative error is usually more informative across different scales.
- Machine precision describes the size of a typical relative rounding error. Many small errors can accumulate; subtraction of nearly equal numbers can cause catastrophic cancellation, while overflow and underflow create additional limits.
- **Conditioning** belongs to the problem: how sensitive is the answer to perturbed input? **Stability** belongs to the algorithm: does the computation amplify rounding errors unnecessarily? A stable algorithm cannot remove intrinsic ill-conditioning.
- If an error behaves like $|e_{n+1}|\approx C|e_n|^p$, then $p$ is its order of convergence. Report both an error estimate and the work needed to achieve it.

## Lecture 2 — bisection and fixed-point iteration

- To solve $f(x)=0$, **bisection** requires continuity and opposite signs at the endpoints. Repeatedly retain the half-interval with a sign change. After $n$ halvings, its width is $(b-a)/2^n$, so the midpoint error is at most half that width. The method is dependable but converges linearly.
- A **fixed point** satisfies $p=g(p)$. The iteration $p_{n+1}=g(p_n)$ converges on an interval if $g$ maps that interval into itself and is a contraction there, for example if $|g'(x)|\le k<1$. Rearranging the same equation into a different $g$ can completely change convergence.
- Stop when the interval width, residual, or successive-step difference meets a justified tolerance; a tiny step by itself does not prove that the true error is tiny.

## Lecture 3 — Newton and secant methods

- **Newton's method** linearizes $f$ near the current estimate: $p_{n+1}=p_n-f(p_n)/f'(p_n)$. Near a simple root, with a suitable starting value and nonzero derivative, convergence is quadratic. Far from the root, or when $f'$ is small, the method can fail.
- **The secant method** replaces the derivative with a slope through the two latest iterates. It needs no derivative evaluation and has local order approximately $(1+\sqrt5)/2$, between linear and quadratic convergence.
- A repeated root generally destroys Newton's quadratic rate. When multiplicity is known, a modified update can restore it; the slides also consider applying Newton's method to $f/f'$. Compare speed with robustness and monitor the residual.

## Lecture 4 — polynomial interpolation

- Distinct nodes $x_0,\ldots,x_n$ determine one polynomial $P_n$ of degree at most $n$ through their data values. Solving for monomial coefficients creates a **Vandermonde system**, which can be badly conditioned even when the interpolating polynomial is mathematically unique.
- The **Lagrange form** avoids first solving for monomial coefficients: $P_n(x)=\sum_{i=0}^n f(x_i)L_i(x)$, where $L_i(x)=\prod_{j\ne i}(x-x_j)/(x_i-x_j)$.
- For sufficiently smooth $f$, the remainder is $f(x)-P_n(x)=f^{(n+1)}(\xi_x)\prod_{i=0}^n(x-x_i)/(n+1)!$. Accuracy depends on both smoothness and node placement; increasing degree alone does not guarantee improvement.

## Lecture 5 — Neville's method and divided differences

- **Neville's method** evaluates successive interpolation polynomials at a chosen $x$ through a recurrence. It is useful when an interpolated value, rather than a full coefficient vector, is needed and when comparing successive degrees.
- **Divided differences** obey $f[x_i,\ldots,x_j]=(f[x_{i+1},\ldots,x_j]-f[x_i,\ldots,x_{j-1}])/(x_j-x_i)$. They give the nested **Newton form**, $P_n(x)=f[x_0]+\sum_{k=1}^n f[x_0,\ldots,x_k]\prod_{j=0}^{k-1}(x-x_j)$, which is easy to extend when new nodes arrive.
- For equally spaced nodes, forward and backward differences provide convenient local formulas near the beginning and end of a table. Node choice still matters: high-degree interpolation at equally spaced nodes may oscillate near endpoints, while Chebyshev points cluster there and control the error-amplification factor.

## Lecture 6 — Hermite interpolation

- **Hermite interpolation** matches values and derivatives at nodes. With both $f(x_i)$ and $f'(x_i)$ at $n+1$ distinct nodes, the unique interpolant has degree at most $2n+1$.
- It can be constructed from Lagrange basis functions or by **repeated nodes** in a divided-difference table. At a repeated node, $f[x_i,x_i]=f'(x_i)$; higher repeated differences encode higher derivatives.
- The extra derivative information improves local matching, but global high-degree polynomial interpolation can remain sensitive to node placement.

## Extra lecture — cubic splines

- A **cubic spline** joins a cubic polynomial on each subinterval and matches the function, first derivative, and second derivative at internal nodes. It gives smooth interpolation without fitting one high-degree polynomial across the whole interval.
- The interval coefficients follow from a tridiagonal linear system for the second-derivative values. A **natural spline** imposes $S''(a)=S''(b)=0$; a **clamped spline** uses specified endpoint slopes $S'(a)$ and $S'(b)$.
- Choose boundary conditions that reflect what is known about the underlying function; the two choices can differ most near the endpoints.

## Lecture 7 — least squares and orthogonal polynomials

- **Interpolation** fits every observation exactly; **least squares** minimizes $\|Ac-y\|_2^2$ and is often more appropriate for noisy measurements. The normal equations are $A^\mathsf{T}Ac=A^\mathsf{T}y$, but their condition number can be much worse than that of $A$; QR-based solution is generally safer.
- For continuous approximation, choose an inner product $\langle u,v\rangle_w=\int_a^b u(x)v(x)w(x)\,dx$. An orthogonal basis simplifies the projection coefficients to $c_k=\langle f,\phi_k\rangle_w/\langle\phi_k,\phi_k\rangle_w$. Gram–Schmidt constructs such a basis from independent functions.
- **Legendre polynomials** are orthogonal on $[-1,1]$ under unit weight. **Chebyshev polynomials** satisfy $T_{n+1}(x)=2xT_n(x)-T_{n-1}(x)$ and are orthogonal under $1/\sqrt{1-x^2}$. Scaled Chebyshev polynomials have a minimax property that motivates Chebyshev interpolation nodes and reduces endpoint amplification.

## Lecture 8 — numerical differentiation

- The forward difference $[f(x+h)-f(x)]/h$ and backward difference are first-order approximations. The centered difference $[f(x+h)-f(x-h)]/(2h)$ is second-order; $[f(x+h)-2f(x)+f(x-h)]/h^2$ approximates $f''(x)$ to second order.
- Smaller $h$ reduces truncation error but magnifies round-off in subtractions and division by $h$. Choose a step size that balances the two sources of error rather than making $h$ arbitrarily small.
- **Richardson extrapolation** cancels a leading error term by combining estimates at $h$ and $h/2$; for a second-order rule, $(4D(h/2)-D(h))/3$ removes the $O(h^2)$ term under suitable smoothness.

## Lecture 9 — trapezoidal and Simpson quadrature

- Numerical quadrature integrates an approximation to $f$. On one interval, the **trapezoidal rule** is $(b-a)[f(a)+f(b)]/2$; **Simpson's rule** is $(b-a)[f(a)+4f((a+b)/2)+f(b)]/6$.
- Composite rules split $[a,b]$ into panels. With sufficient smoothness, composite trapezoidal error is $O(h^2)$ and composite Simpson error is $O(h^4)$; Simpson's rule requires an even number of equal subintervals. Their error bounds involve $f''$ and $f^{(4)}$, respectively.
- The **degree of precision** is the highest polynomial degree integrated exactly. Trapezoidal and Simpson rules have degrees 1 and 3. They are closed Newton–Cotes formulas because their nodes include the panel endpoints.

## Lecture 10 — adaptive and Gaussian quadrature

- **Adaptive Simpson quadrature** subdivides where the integrand varies rapidly. Compare one Simpson estimate on a panel with the sum on its two halves; their difference divided by 15 estimates the finer result's error under the usual smoothness assumptions. Allocate tolerances across subintervals and stop only when local error targets are met.
- **Gaussian quadrature** chooses both nodes and weights to maximize polynomial exactness. An $n$-node Gauss–Legendre rule uses the roots of $P_n$ and integrates polynomials of degree at most $2n-1$ exactly on $[-1,1]$.
- Map a general interval $[a,b]$ to $[-1,1]$ before using the standard nodes and weights. Smoothness and endpoint behavior determine whether a high-order rule is effective.

## Lecture 11 — initial-value problems and Euler's method

- For $y'=f(t,y)$ and $y(a)=\alpha$, continuity together with a Lipschitz condition in $y$ provides a standard uniqueness guarantee. The Lipschitz constant also controls how perturbations can grow.
- **Euler's method** uses $w_{i+1}=w_i+h f(t_i,w_i)$. It follows the tangent slope over each step; under standard smoothness and stability assumptions its one-step defect is $O(h^2)$ and its global error is $O(h)$.
- Smaller $h$ generally improves truncation accuracy but increases the number of steps and possible rounding effects. Compare numerical results at several step sizes rather than trusting a single run.

## Lecture 12 — Taylor and Runge–Kutta methods

- A higher-order **Taylor method** retains more terms in the solution's time expansion, but higher derivatives of $f$ can be expensive to derive. The normalized local truncation error helps predict a method's global order.
- **Second-order Runge–Kutta methods** such as midpoint and modified Euler (Heun) use an extra slope evaluation to improve on Euler without explicitly computing higher derivatives.
- **Classical RK4** combines four slopes with weights $1,2,2,1$: $w_{i+1}=w_i+h(k_1+2k_2+2k_3+k_4)/6$, where the slopes are evaluated at the beginning, two midpoints, and the end of the step. It has fourth-order global accuracy for a sufficiently smooth solution.

## Lecture 13 — multistep methods, consistency, and stability

- **Multistep methods** reuse earlier values and slopes. Adams–Bashforth methods are explicit; Adams–Moulton methods are implicit and require solving for the new value. Both need starting values, often obtained from a one-step method such as RK4.
- An implicit method can improve stability, but it introduces an equation to solve at each step. Higher formal order alone does not guarantee a reliable computation.
- **Consistency** means the local truncation error vanishes as $h\to0$. **Stability** means small perturbations in starting values or arithmetic do not grow uncontrollably. Together they explain convergence under the method's assumptions; monitor both when choosing a step size.

## Practical checklist

1. Identify the target quantity and error measure before choosing a method.
2. Check smoothness, node distribution, conditioning, and boundary information.
3. Prefer numerically stable representations and solvers; test whether results change under a smaller step size or a different basis.
4. Report the residual or estimated error together with computational cost, and distinguish numerical error from modeling assumptions.
{% endraw %}
