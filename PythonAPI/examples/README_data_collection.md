# BehaviorAgent Data Collection for Bench2Drive

This directory contains tools for collecting autonomous driving datasets using CARLA's BehaviorAgent in the Bench2Drive format.

## Overview

The data collection system consists of three main components:

1. **SensorManager** (`carla/agents/tools/sensor_manager.py`) - Manages all sensors attached to the vehicle
2. **DataCollector** (`carla/agents/tools/data_collector.py`) - Collects and saves data in Bench2Drive format
3. **Example Script** (`behavior_agent_data_collection.py`) - Demonstrates complete data collection workflow

## Features

- **360° Sensor Coverage**: 6 RGB cameras + 1 top-down camera for full visibility
- **Multi-Modal Data**: RGB, depth, semantic segmentation, instance segmentation, and LiDAR
- **Bench2Drive Compatible**: Data saved in B2D format for easy integration with existing datasets
- **Behavior Profiles**: Collect data with cautious, normal, or aggressive driving behaviors
- **CAN Bus Telemetry**: Vehicle state, control inputs, and navigation data
- **Traffic Simulation**: Configurable number of AI vehicles and pedestrians

## Quick Start

### Prerequisites

- CARLA 0.9.15 running on localhost (or specify `--host`)
- Python 3.7+
- Required Python packages: numpy, PIL

### Basic Usage

#### With Display (Local Machine)

```bash
# Start CARLA server first
./CarlaUE5.sh

# In another terminal, run data collection
cd PythonAPI/examples
python behavior_agent_data_collection.py \
    --town Town01 \
    --behavior normal \
    --weather 0 \
    --max-frames 1000 \
    --output-dir ./my_dataset
```

#### Headless Mode (Server/No Display)

For server-based data collection without display:

```bash
# Start CARLA in headless mode (offscreen rendering)
SDL_VIDEODRIVER=offscreen ./CarlaUE5.sh -RenderOffScreen

# Alternative: Use xvfb (virtual framebuffer)
xvfb-run -a ./CarlaUE5.sh

# Or with explicit display settings
DISPLAY= ./CarlaUE5.sh -RenderOffScreen -nosound -carla-rpc-port=2000

# In another terminal/tmux session, run data collection
cd PythonAPI/examples
python behavior_agent_data_collection.py \
    --sync \
    --town Town01 \
    --behavior normal \
    --weather 0 \
    --max-frames 1000 \
    --output-dir /path/to/storage/b2d_dataset
```

**Important Notes for Headless Mode:**
- Use `--sync` flag for better stability in headless mode
- Specify absolute paths for `--output-dir` (e.g., `/data/datasets/b2d`)
- Monitor disk space - each 1000 frames uses ~1-2 GB
- Use `tmux` or `screen` for persistent sessions
- Check logs: CARLA logs are in `$CARLA_ROOT/Build/LinuxNoEditor/CarlaUE5/Saved/Logs/`

### Advanced Usage

```bash
python behavior_agent_data_collection.py \
    --host 127.0.0.1 \
    --port 2000 \
    --sync \
    --town Town03 \
    --behavior aggressive \
    --weather 5 \
    --route-id 42 \
    --max-frames 5000 \
    --num-vehicles 50 \
    --num-pedestrians 20 \
    --output-dir /path/to/dataset
```

## Command Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--host` | 127.0.0.1 | IP address of CARLA server |
| `--port` | 2000 | TCP port for CARLA connection |
| `--tm-port` | 8000 | Traffic Manager port |
| `--sync` | False | Enable synchronous mode (recommended) |
| `--behavior` | normal | Driving behavior profile (see table below) |
| `--town` | Town01 | Map/town to load |
| `--weather` | 0 | Weather preset ID (0-13) |
| `--route-id` | 1 | Route number for dataset naming |
| `--output-dir` | ./b2d_dataset | Root directory for dataset |
| `--max-frames` | 1000 | Maximum frames to collect |
| `--num-vehicles` | 30 | Number of traffic vehicles |
| `--num-pedestrians` | 10 | Number of pedestrians |

### Behavior Profiles

The system supports 11 different driving behavior profiles for diverse dataset collection:

#### Original Behaviors (3)

| Profile | Command | Speed | Risk | Characteristics |
|---------|---------|-------|------|-----------------|
| **Cautious** | `cautious` | Low | Very Low | Conservative, follows rules closely |
| **Normal** | `normal` | Medium | Medium | Standard balanced driving |
| **Aggressive** | `aggressive` | High | High | Fast, pushy, impatient |

#### Extended Psychological Profiles (8)

| Profile | Command | Speed | Risk | Key Traits |
|---------|---------|-------|------|------------|
| **Steady Veteran** | `steady_veteran` | Very Low | Lowest | Very cautious, rule-following, smooth braking, mindful |
| **Urban Daredevil** | `urban_daredevil` | Highest | High | Confident, rule-breaking, efficient, aggressive |
| **Confident Cruiser** | `confident_cruiser` | Medium-High | Medium | Efficient, good interaction, attentive, rule-bending |
| **Mindful Navigator** | `mindful_navigator` | Medium-Low | Low | Cautious, very attentive, smooth braking, rule-following |
| **Bold Rookie** | `bold_rookie` | High | High | Confident, abrupt braking, aggressive, less mindful |
| **Uncertain Sprinter** | `uncertain_sprinter` | High | Highest | Inconsistent, inattentive, inefficient, risky |
| **Chill Maverick** | `chill_maverick` | High | Medium | Casual, rule-bending, efficient, smooth but pushy |
| **Balanced Driver** | `balanced_driver` | Medium | Low | Average in all aspects, balanced reactions |

**Usage Examples:**

```bash
# Collect data with the safest driver
python behavior_agent_data_collection.py --behavior steady_veteran --max-frames 2000

# Collect data with the riskiest driver
python behavior_agent_data_collection.py --behavior uncertain_sprinter --max-frames 2000

# Collect data across all profiles (bash loop)
for behavior in cautious normal aggressive steady_veteran urban_daredevil \
                confident_cruiser mindful_navigator bold_rookie \
                uncertain_sprinter chill_maverick balanced_driver; do
    python behavior_agent_data_collection.py \
        --behavior $behavior \
        --route-id 1 \
        --max-frames 1000 \
        --sync \
        --output-dir /data/b2d_dataset
done
```

## Dataset Structure

The collected data follows the Bench2Drive format:

```
output_dir/
└── GeneralDriving_Town01_Route001_Weather00/
    ├── anno/
    │   ├── 00000.json.gz
    │   ├── 00001.json.gz
    │   └── ...
    ├── camera/
    │   ├── rgb_front/
    │   │   ├── 00000.jpg
    │   │   └── ...
    │   ├── rgb_front_left/
    │   ├── rgb_front_right/
    │   ├── rgb_back/
    │   ├── rgb_back_left/
    │   ├── rgb_back_right/
    │   ├── rgb_top_down/
    │   ├── depth_front/
    │   │   ├── 00000.png
    │   │   └── ...
    │   ├── depth_front_left/
    │   ├── ... (depth for all 6 cameras)
    │   ├── semantic_front/
    │   │   ├── 00000.png
    │   │   └── ...
    │   ├── ... (semantic for all 6 cameras)
    │   ├── instance_front/
    │   │   ├── 00000.png
    │   │   └── ...
    │   └── ... (instance for all 6 cameras)
    └── lidar/
        ├── 00000.ply
        ├── 00001.ply
        └── ...
```

## Sensor Configuration

### Cameras (Bench2Drive Preset)

| Camera | Position (x, y, z) | Rotation (yaw) | Resolution | FOV |
|--------|-------------------|----------------|------------|-----|
| Front | (0.80, 0.0, 1.60) | 0° | 1600x900 | 70° |
| Front Left | (0.27, -0.55, 1.60) | -55° | 1600x900 | 70° |
| Front Right | (0.27, 0.55, 1.60) | 55° | 1600x900 | 70° |
| Back | (-2.0, 0.0, 1.60) | 180° | 1600x900 | 110° |
| Back Left | (-0.32, -0.55, 1.60) | -110° | 1600x900 | 70° |
| Back Right | (-0.32, 0.55, 1.60) | 110° | 1600x900 | 70° |
| Top Down | (0.0, 0.0, 50.0) | 0° (pitch: -90°) | 1600x900 | 90° |

Each RGB camera has corresponding depth, semantic segmentation, and instance segmentation cameras at the same position.

### LiDAR

- **Position**: (-0.39, 0.0, 1.84)
- **Range**: 85 meters
- **Channels**: 64
- **Rotation Frequency**: 10 Hz
- **Points per Second**: 600,000

### Other Sensors

- **IMU**: 20 Hz sampling rate
- **GNSS**: Global positioning
- **Speedometer**: 20 Hz reading frequency

### Image Format Details

**RGB Images (`.jpg`):**
- Standard RGB color images
- JPEG format with 95% quality
- Resolution: 1600x900

**Depth Images (`.png`):**
- Encoded depth information in RGB channels
- Use CARLA depth conversion formulas to decode actual depth values
- Logarithmic encoding for better precision at long distances

**Semantic Segmentation (`.png`):**
- **CityScapes color palette** for visual interpretation
- Each class has a distinct color for easy visualization:
  - Road: Purple `(128, 64, 128)`
  - Sidewalk: Pink `(244, 35, 232)`
  - Building: Gray `(70, 70, 70)`
  - Vegetation: Green `(107, 142, 35)`
  - Vehicle: Dark Blue `(0, 0, 142)`
  - Pedestrian: Red `(220, 20, 60)`
  - Sky: Light Blue `(70, 130, 180)`
  - And more...
- **Visually readable** without post-processing
- Can be converted back to class IDs using CityScapes color mapping if needed

**Instance Segmentation (`.png`):**
- Each object instance has a **unique ID**
- Instance ID encoded in **red channel** (R value)
- Format: `instance_id = pixel[R]`
- Different vehicles/pedestrians have different IDs
- Allows tracking individual objects across frames
- Example: Extract all pixels belonging to vehicle #5: `mask = (image[:,:,0] == 5)`

## Annotation Data Format

Each `anno/*.json.gz` file contains:

```json
{
  "x": 123.45,                    // Global X position
  "y": 67.89,                     // Global Y position
  "theta": 1.57,                  // Heading angle (radians)
  "speed": 8.5,                   // Speed (m/s)
  "acceleration": [0.1, 0.0, -9.8], // 3-axis acceleration
  "angular_velocity": [0.0, 0.0, 0.05], // 3-axis angular velocity
  "throttle": 0.5,                // Throttle [0.0, 1.0]
  "steer": -0.1,                  // Steering [-1.0, 1.0]
  "brake": 0.0,                   // Brake [0.0, 1.0]
  "reverse": false,               // Reverse gear
  "weather": 0,                   // Weather ID
  "x_command_far": 150.0,         // Far waypoint X
  "y_command_far": 80.0,          // Far waypoint Y
  "command_far": 2,               // Far command
  "x_command_near": 130.0,        // Near waypoint X
  "y_command_near": 75.0,         // Near waypoint Y
  "command_near": 2,              // Near command
  "x_target": 200.0,              // Target X
  "y_target": 100.0,              // Target Y
  "next_command": 3,              // Next navigation command
  "should_brake": false,          // Whether to brake
  "only_ap_brake": false,         // Autopilot brake only
  "bounding_boxes": {},           // 3D bounding boxes (optional)
  "sensors": {}                   // Sensor calibration (optional)
}
```

## Weather Presets

| ID | Weather |
|----|---------|
| 0 | Clear Noon |
| 1 | Cloudy Noon |
| 2 | Wet Noon |
| 3 | Wet Cloudy Noon |
| 4 | Mid Rainy Noon |
| 5 | Hard Rain Noon |
| 6 | Soft Rain Noon |
| 7 | Clear Sunset |
| 8 | Cloudy Sunset |
| 9 | Wet Sunset |
| 10 | Wet Cloudy Sunset |
| 11 | Mid Rain Sunset |
| 12 | Hard Rain Sunset |
| 13 | Soft Rain Sunset |

## Programmatic Usage

```python
from agents.navigation.behavior_agent import BehaviorAgent
from agents.tools.sensor_manager import SensorManager
from agents.tools.data_collector import DataCollector

# Create vehicle and agent
vehicle = world.spawn_actor(blueprint, spawn_point)
agent = BehaviorAgent(vehicle, behavior='normal')

# Setup sensors
sensor_manager = SensorManager(vehicle, config_preset='bench2drive')

# Setup data collector
data_collector = DataCollector(
    sensor_manager=sensor_manager,
    vehicle=vehicle,
    root_dir='./dataset',
    scenario_type='GeneralDriving',
    town='Town01',
    route_id=1,
    weather_id=0
)

# Set destination
agent.set_destination(destination)

# Start recording
data_collector.start_recording()

# Main loop
while not agent.done():
    control = agent.run_step()
    vehicle.apply_control(control)
    data_collector.record_frame(control=control)
    world.tick()

# Stop and cleanup
data_collector.stop_recording()
sensor_manager.destroy()
```

## Tips for Large-Scale Data Collection

### General Best Practices

1. **Use Synchronous Mode**: Add `--sync` flag for deterministic behavior and consistency
2. **Adjust Traffic**: Vary `--num-vehicles` and `--num-pedestrians` for diversity
3. **Multiple Runs**: Collect multiple routes with different weather conditions
4. **Disk Space**: Ensure sufficient storage (~1-2 GB per 1000 frames)
5. **Performance**: For better FPS, reduce number of traffic vehicles or use headless mode

### Server Deployment (Headless Mode)

For large-scale data collection on servers without displays:

#### 1. **Setup Virtual Display (Recommended)**

```bash
# Install xvfb
sudo apt-get install xvfb

# Create a systemd service for CARLA
cat > /etc/systemd/system/carla.service <<EOF
[Unit]
Description=CARLA Simulator Server
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/CARLA
ExecStart=/usr/bin/xvfb-run -a /path/to/CARLA/CarlaUE5.sh -RenderOffScreen -nosound -carla-rpc-port=2000
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Start the service
sudo systemctl daemon-reload
sudo systemctl start carla
sudo systemctl enable carla  # Auto-start on boot
```

#### 2. **Tmux Session Management**

```bash
# Start persistent tmux session
tmux new -s carla_data_collection

# In tmux, start CARLA server
SDL_VIDEODRIVER=offscreen ./CarlaUE5.sh -RenderOffScreen -nosound

# Split window (Ctrl+B, %)
# In new pane, run data collection
cd PythonAPI/examples
python behavior_agent_data_collection.py \
    --sync \
    --behavior normal \
    --town Town01 \
    --weather 0 \
    --max-frames 10000 \
    --output-dir /mnt/storage/b2d_dataset

# Detach: Ctrl+B, D
# Reattach later: tmux attach -t carla_data_collection
```

#### 3. **Batch Collection Script**

Create a script to collect data for all behaviors and weather conditions:

```bash
#!/bin/bash
# collect_all_data.sh

OUTPUT_DIR="/data/b2d_dataset"
TOWNS=("Town01" "Town02" "Town03" "Town04" "Town05")
WEATHERS=(0 1 2 3 4 5 6 7 8 9 10 11 12 13)
BEHAVIORS=(cautious normal aggressive steady_veteran urban_daredevil \
           confident_cruiser mindful_navigator bold_rookie \
           uncertain_sprinter chill_maverick balanced_driver)
MAX_FRAMES=5000
ROUTE_ID=1

for town in "${TOWNS[@]}"; do
    for weather in "${WEATHERS[@]}"; do
        for behavior in "${BEHAVIORS[@]}"; do
            echo "Collecting: $town, Weather $weather, Behavior $behavior"

            python behavior_agent_data_collection.py \
                --sync \
                --town "$town" \
                --weather "$weather" \
                --behavior "$behavior" \
                --route-id "$ROUTE_ID" \
                --max-frames "$MAX_FRAMES" \
                --num-vehicles 30 \
                --output-dir "$OUTPUT_DIR" \
                2>&1 | tee -a "logs/collection_${town}_${weather}_${behavior}.log"

            # Increment route ID
            ROUTE_ID=$((ROUTE_ID + 1))

            # Optional: Add delay between runs
            sleep 10
        done
    done
done

echo "Data collection complete! Total scenarios: $((${#TOWNS[@]} * ${#WEATHERS[@]} * ${#BEHAVIORS[@]}))"
```

#### 4. **Monitoring & Logging**

```bash
# Create logs directory
mkdir -p logs

# Monitor CARLA server logs
tail -f $CARLA_ROOT/Build/LinuxNoEditor/CarlaUE5/Saved/Logs/CarlaUE5.log

# Monitor disk usage
watch -n 60 'df -h /data/b2d_dataset'

# Monitor collection progress
watch -n 10 'find /data/b2d_dataset -name "*.jpg" | wc -l'
```

#### 5. **Resource Management**

```bash
# Limit GPU usage (if needed)
export CUDA_VISIBLE_DEVICES=0  # Use specific GPU

# Set process priority
nice -n 10 ./CarlaUE5.sh -RenderOffScreen  # Lower priority

# Limit memory (using cgroups)
cgexec -g memory:carla_limit ./CarlaUE5.sh
```

#### 6. **Data Validation**

After collection, validate the dataset:

```bash
# Check for incomplete scenarios
for dir in /data/b2d_dataset/*/; do
    anno_count=$(ls "$dir/anno/" 2>/dev/null | wc -l)
    rgb_count=$(ls "$dir/camera/rgb_front/" 2>/dev/null | wc -l)

    if [ "$anno_count" -ne "$rgb_count" ]; then
        echo "WARNING: Mismatch in $dir (anno: $anno_count, rgb: $rgb_count)"
    fi
done

# Check disk usage per scenario
du -sh /data/b2d_dataset/*/ | sort -h
```

## Known Limitations

1. LiDAR data is saved as `.ply` files (can be converted to `.laz` offline for compression)
2. Bounding boxes and sensor calibration data are placeholders (to be implemented)
3. Waypoint information requires integration with navigation system

## Troubleshooting

**Issue**: Low FPS during collection
- Solution: Reduce `--num-vehicles`, enable `--sync`, or use headless CARLA

**Issue**: Sensors not initializing
- Solution: Wait a few ticks after spawning vehicle, check CARLA server logs

**Issue**: Missing sensor data in some frames
- Solution: This warning is normal for first few frames, sensors initialize asynchronously

**Issue**: Out of disk space
- Solution: Monitor disk usage, each 1000-frame collection uses ~1-2 GB

## Future Enhancements

- [ ] Add bounding box extraction for nearby vehicles/pedestrians
- [ ] Include sensor intrinsic/extrinsic calibration matrices
- [ ] Support for multiple ego vehicles (multi-agent scenarios)
- [ ] Real-time visualization of collected data
- [ ] Automatic `.ply` to `.laz` conversion for LiDAR
- [ ] Resume collection from checkpoint
- [ ] Dataset statistics and validation tools

## References

- [CARLA Documentation](https://carla.readthedocs.io/)
- [Bench2Drive Dataset](https://github.com/Thinklab-SJTU/Bench2Drive)
- [BehaviorAgent API](https://carla.readthedocs.io/en/latest/adv_agents/)

## License

This work is licensed under the terms of the MIT license.
