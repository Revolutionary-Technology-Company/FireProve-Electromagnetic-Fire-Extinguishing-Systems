## 1. Pyramidal Acoustic Orientation

* Elevation Traded Offsets: Two microphones angled 45° upward and two angled 45° downward provide maximum geometric vertical separation.
* Azimuth Cross-Over: Pair the elevation shifts with a 90° horizontal cross-mounting to allow simultaneous 3D spherical localization.
* Chassis Isolation: Mount microphones inside acoustic isolating dampening rings to prevent turret motor vibrations from fouling the inputs.

## 2. TDoA Matrix (Hexadecimal Array Calibration)

* Z-Axis Extraction: Comparing the Time Difference of Arrival (TDoA) between the upper and lower pairs immediately yields the target elevation angle.
* Vector Streaming: Telemetry feeds directly into the native 16-state analog logic processor at extreme speed.
* Voltage State Tuning: Signal delays map onto discrete 0.0V–1.0V voltage levels for zero-latency angular tracking.

## 3. Coordinate Translation Matrix

       [ Mic 1: +45° Up, Left ]     [ Mic 2: +45° Up, Right ]
                     \               /
                      \   (Boresight)
                      /              \
       [ Mic 3: -45° Down, Left ]   [ Mic 4: -45° Down, Right ]


* Elevation Formula: $\Delta t_{\text{vertical}} = (t_{\text{Mic1}} + t_{\text{Mic2}}) - (t_{\text{Mic3}} + t_{\text{Mic4}})$
* Azimuth Formula: $\Delta t_{\text{horizontal}} = (t_{\text{Mic1}} + t_{\text{Mic3}}) - (t_{\text{Mic2}} + t_{\text{Mic4}})$
* Servo Correction: The resultant error vector drives the dual-axis gimbals until $\Delta t_{\text{vertical}}$ and $\Delta t_{\text{horizontal}}$ reach zero (perfect lock).
