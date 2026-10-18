# Independent review of binary-model numerical acceptance

Reviewed candidate: `analysis/nested_logit.py`, SHA256 `ab8c609c131888d2a90b13737841fb6f6a636172a3cf669c3c8a76d8529c57e8`. This is a static review and fixed-parameter verification, not acceptance of a fit that has not yet been saved.

The implementation fits the declared frequentist nested Bernoulli model. The likelihood groups actor counts without adding binomial constants; frequency compression and row reordering are independently checked. It correctly uses the numerical derivative of the evaluated adaptive quadrature target for its final polish. The integrated score used during warmup is not exactly that derivative at finite quadrature points, a distinction confirmed by the fixtures. A warmup precision-loss message does not itself establish failure or convergence of the final polished solution.

An inverse observed Hessian is a valid information-based covariance estimate for the candidate's evaluated likelihood at a regular interior solution. The script uses central numerical differences at absolute step2e-4 and requires a positive minimum eigenvalue. This needs a step-size check because too small a step amplifies integration/roundoff noise and too large a step biases curvature. An independent checker implements central second differences directly and compares steps1e-4,2e-4,4e-4, standard errors, eigenvalues and condition numbers.

The existing final acceptance rule requires finite parameters, gradient infinity norm below0.005 and minimum Hessian eigenvalue above1e-5. These are useful checks but are not equivalent to Stata's documented scaled-gradient rule. A small unscaled gradient can conceal a material remaining Newton step in a flat variance direction. The relevant additional diagnostic is `gradient' * covariance * gradient`, compared with1e-5 as the general [Stata16 maximize](https://www.stata.com/manuals16/rmaximize.pdf), p.3 scaled-gradient tolerance. Interpret this with Hessian stability and the objective change; do not infer the original executable's complete stopping rule from a general manual default.

The independent post-fit command is:

```powershell
rtk proxy .\.venv\Scripts\python.exe tests/skill2/check_glmm_fit_curvature.py --fit <fit-json>
```

It does no optimization and writes `<model_id>_independent_curvature.json` under this diagnostics folder. It independently recodes the unchanged raw data and differentiates the currently loaded production likelihood. It must be run on the final saved vector; it is not implied by synthetic tests. A higher-point integral check is separately required to quantify quadrature error; a converged seven-point target need not equal the exact integrated maximum or another software's finite quadrature target.

Performance observation: the current batch log's score search approaches negative log likelihood663.2791800500565 for M2 and reports precision loss, then enters finite-difference polish. That stage has no callbacks in this version, so the lack of new stdout cannot diagnose a stall. No running engine was edited by this verifier. The root implementer changed unconditional damping to full moment updates for the first20 iterations with damping only afterward; the final source passed the regenerated fixed-parameter fixture checks.
