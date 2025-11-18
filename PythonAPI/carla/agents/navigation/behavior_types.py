# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
This module contains the different parameters sets for each behavior.

Original Behaviors:
- Cautious: Conservative driving, follows rules
- Normal: Standard driving behavior
- Aggressive: Fast, pushy driving

Extended Behaviors (Psychological Driver Profiles):
- SteadyVeteran: Very cautious, rule-following, efficient, lowest risk
- UrbanDaredevil: Confident, rule-breaking, aggressive, highest efficiency
- ConfidentCruiser: Slightly cautious, efficient, rule-breaking, good interaction
- MindfulNavigator: Cautious, efficient, rule-following, very attentive
- BoldRookie: Confident, abrupt braking, aggressive, high risk
- UncertainSprinter: Inconsistent, inattentive, inefficient, highest risk
- ChillMaverick: Confident, rule-bending, efficient, aggressive but casual
- BalancedDriver: Somewhat cautious, efficient, rule-following, average
"""


# ============================================================================
# ORIGINAL BEHAVIORS (for backwards compatibility)
# ============================================================================

class Cautious(object):
    """Class for Cautious agent."""
    max_speed = 40
    speed_lim_dist = 6
    speed_decrease = 12
    safety_time = 3
    min_proximity_threshold = 12
    braking_distance = 6
    tailgate_counter = 0


class Normal(object):
    """Class for Normal agent."""
    max_speed = 50
    speed_lim_dist = 3
    speed_decrease = 10
    safety_time = 3
    min_proximity_threshold = 10
    braking_distance = 5
    tailgate_counter = 0


class Aggressive(object):
    """Class for Aggressive agent."""
    max_speed = 70
    speed_lim_dist = 1
    speed_decrease = 8
    safety_time = 3
    min_proximity_threshold = 8
    braking_distance = 4
    tailgate_counter = -1


# ============================================================================
# EXTENDED BEHAVIORS (Psychological Driver Profiles)
# ============================================================================

class SteadyVeteran(object):
    """
    The Steady Veteran

    HABITS:
    Very cautious, sticks to the rules, mindful of other drivers and efficient
    (smooth braking). The lowest in risk taking among the other behaviors.

    REACTION:
    Takes the safest option (braking, stopping).
    """
    max_speed = 35              # Very cautious speed
    speed_lim_dist = 8          # Well below speed limit
    speed_decrease = 15         # Smooth, gradual braking
    safety_time = 4.0           # High safety buffer
    min_proximity_threshold = 15  # Large safe distance
    braking_distance = 8        # Early emergency braking
    tailgate_counter = 0        # Never tailgates


class UrbanDaredevil(object):
    """
    The Urban Daredevil

    HABITS:
    Confident, mostly efficient (smooth braking), not hesitating to break rules,
    sometimes aggressive/pushy. Highest score in efficiency, lowest in attention.

    REACTION:
    Drives carefully in general but takes significantly more risk than Steady Veteran.
    """
    max_speed = 80              # Highest speed
    speed_lim_dist = 0          # Doesn't care about speed limit
    speed_decrease = 6          # Efficient but aggressive
    safety_time = 2.5           # Lower safety buffer
    min_proximity_threshold = 7 # Close following
    braking_distance = 3        # Late braking
    tailgate_counter = -1       # Aggressive lane changing


class ConfidentCruiser(object):
    """
    The Confident Cruiser

    HABITS:
    Little cautious, efficient (smooth braking), not hesitating to break the rules.
    Highest score in interaction, high score in attention, efficiency and
    self-efficacy, average in risk-taking.

    REACTION:
    Sensitive to varying distances (video variations) and good level of risk awareness.
    """
    max_speed = 60              # Moderately fast
    speed_lim_dist = 2          # Slightly above limit
    speed_decrease = 9          # Efficient, smooth
    safety_time = 2.8           # Moderate safety
    min_proximity_threshold = 9 # Reasonable distance
    braking_distance = 4.5      # Moderate braking
    tailgate_counter = 0        # Good interaction, doesn't push


class MindfulNavigator(object):
    """
    The Mindful Navigator

    HABITS:
    Cautious, mostly efficient (smooth braking), sticks to the rules, slightly
    less collaboration with other road users. High scores in attention, average
    in most others.

    REACTION:
    Very attentive, also sensitive to varying distances.
    """
    max_speed = 45              # Cautious speed
    speed_lim_dist = 5          # Below speed limit
    speed_decrease = 12         # Smooth, efficient braking
    safety_time = 3.5           # Good safety buffer
    min_proximity_threshold = 12  # Safe distance
    braking_distance = 6        # Early braking
    tailgate_counter = 0        # Doesn't tailgate


class BoldRookie(object):
    """
    The Bold Rookie

    HABITS:
    Somewhat confident, less mindful of other drivers, less efficient (abrupt
    braking), mostly sticks to the rules, but somewhat aggressive/pushy, less
    collaboration with other road users. High score in risk taking, low in
    attention and efficiency.

    REACTION:
    Takes higher risk, sometimes appearing aggressive.
    """
    max_speed = 65              # Fast but not highest
    speed_lim_dist = 1          # Slightly over limit
    speed_decrease = 5          # Abrupt, inefficient braking
    safety_time = 2.2           # Lower safety buffer
    min_proximity_threshold = 7.5  # Close following
    braking_distance = 3.5      # Late braking
    tailgate_counter = -1       # Aggressive, pushy


class UncertainSprinter(object):
    """
    The Uncertain Sprinter

    HABITS:
    Inconsistent answers (always disagree); somewhat sticking to the rules yet
    inattentive and also inefficient. Highest scores in risk taking, lowest in
    efficiency and interaction, also low in self efficacy and attention.

    REACTION:
    Indifferent driving behavior regardless of the distance between themselves
    and the other vehicle. Partly inconsistent reactions, in general high risk taking.
    """
    max_speed = 75              # High speed, inconsistent
    speed_lim_dist = 0          # Inattentive to rules
    speed_decrease = 4          # Very inefficient, abrupt
    safety_time = 2.0           # Lowest safety buffer
    min_proximity_threshold = 6.5  # Closest following distance
    braking_distance = 3        # Late, risky braking
    tailgate_counter = -1       # Aggressive, inconsistent


class ChillMaverick(object):
    """
    The Chill Maverick

    HABITS:
    Confident, likes to bend the rules, mindful of other drivers, very efficient
    (smooth braking), but also very aggressive/pushy. Highest scores in efficiency,
    also high in interaction, lowest in attention, average in risk taking.

    REACTION:
    More casual driving style, takes slightly higher risk, not very sensitive to
    varying distances.
    """
    max_speed = 70              # Fast but controlled
    speed_lim_dist = 1          # Bends rules
    speed_decrease = 8          # Very efficient, smooth
    safety_time = 2.6           # Moderate-low safety
    min_proximity_threshold = 8.5  # Comfortable with close following
    braking_distance = 4        # Moderate braking
    tailgate_counter = -1       # Aggressive but smooth


class BalancedDriver(object):
    """
    The Balanced Driver

    HABITS:
    Somewhat cautious, mindful of other drivers, efficient. Generally sticks
    to the rules. Low in risk taking, average in other categories.

    REACTION:
    Reactions balanced and around the average of results for other clusters.
    """
    max_speed = 50              # Average speed
    speed_lim_dist = 4          # Slightly below limit
    speed_decrease = 10         # Balanced braking
    safety_time = 3.0           # Standard safety
    min_proximity_threshold = 10  # Standard distance
    braking_distance = 5        # Standard braking
    tailgate_counter = 0        # Doesn't tailgate
