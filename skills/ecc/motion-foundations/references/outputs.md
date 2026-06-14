## Outputs

This skill produces:

- A shared `motionTokens` object (duration, easing, distance, scale)
- A shared `springs` preset map (5 named configs)
- A `shouldAnimate()` gate used by all components
- Accessibility-compliant animation defaults via `useReducedMotion`
- SSR-safe initial states with zero hydration warnings