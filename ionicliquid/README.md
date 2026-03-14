# Simulation of an ionic liquid

## Objectives

The following example uses molecular dynamics (MD) simulations to study an ionic liquid, butylmethylimidazolium bis(trifluoromethanesulfonyl)imide). Ionic liquids are entirely composed of large organic ions. Their asymmetric shspe, molecular flexilibity and charge delocalization render crystallization difficult, therefore these compounds have melting points below room temperature. They are molten salts, with negligible volatility, and interesting as novel solvents for chemical reactions or separations, or as electrolytes for energy-storage devices.

Ionic liquids are considerably more viscous than organic solvents, so trajectories need to be longer and it is interesting to run then at ghigher temperatures (353 K for example).

When building a simulation box, make sure the total charge is zero (same number of cations and anions). The example ions provided are in the `c4c1im.zmat` (cation) and `ntf2.zmat` (anion).
