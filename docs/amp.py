This custom, high-current Class-D amplifier is optimized for high-power sub-bass (30 Hz–60 Hz) delivery into the low-impedance titanium compression driver, using the RT Architecture guidelines for thermal and noise isolation.
## 1. Architectural Block Diagram

 [ 0-1V Hex Input ] ---> [ RT Analog Buffer/Filter ] ---> [ PWM Controller (TI TPA3255 Class-D) ]
                                                                       |
 [ High-Voltage DC ] ---> [ GaN FET Half-Bridge Output Stage ] <-------+
                                        |
                        [ Heavy-Duty LC Low-Pass Filter ] 
                                        |
                        [ 4.8" Titanium Driver Terminal ]

## 2. Core Schematic Sub-Systems## A. Input & Modulation Stage

* Analog Interface: Differential input lines accept the 0.0V–1.0V tracking signals.
* PWM Modulation: Employs a high-frequency carrier (400 kHz–500 kHz) to drive switching cycles.
* Dead-Time Control: Strict hardware dead-time prevention avoids shoot-through in the output stage.

## B. GaN FET Power Output Stage

* Switching Element: Gallium Nitride (GaN) FETs replace silicon MOSFETs for ultra-fast switching speeds.
* Efficiency: Minimizes switching losses, reducing radiant heat near the turret base.
* Power Rails: Tied to a dedicated high-voltage DC supply rail (typically 48V–50V).

## C. Heavy-Duty LC Low-Pass Filter

* High-Current Inductors: Dual toroid inductors wound with thick copper wire to prevent magnetic saturation.
* Filter Capacitors: High-voltage metal film capacitors remove the high-frequency PWM switching carrier.
* Output Path: Delivers a clean, continuous sine wave to the titanium voice coil.

## 3. KiCad Layout & Trace Routing Strategy

# Layout rule snippet for rt_amplifier_layout.pydef enforce_amplifier_constraints(board):
    # Enforce 3oz copper zones for power delivery paths
    # Keep switching GaN FET loops as short as physically possible
    # Place output LC filter immediately adjacent to FET outputs
    # Ground planes segregated: Analog Ground isolated from Power Ground via star point
    pass


* Power Paths: Implements thick 3oz copper pours for high-current loops to prevent thermal stress.
* Loop Minimization: Keeps the trace paths between GaN FETs and decoupling capacitors under 5 mm.
* Ground Isolation: Segregates sensitive analog inputs from noisy high-power grounds via a single-point star ground.

