#我要推出距离1-21的最佳排序 +是加速度1 -是减速度1 o是匀速
#排序+-o然后是curr_distance等于目标距离 并且速度是0
# Function to generate the optimal sequence of actions
def generate_optimal_sequence(n):
    optimal_sequence = []
    # Start with maximum distance and velocity
    curr_distance = n
    velocity = 0
    
    while curr_distance > 0 or velocity != 0:
        if curr_distance - velocity > 0:
            optimal_sequence.append('+')  # Accelerate to reduce remaining distance
            velocity += 1
            curr_distance -= velocity
        elif curr_distance - velocity < 0:
            optimal_sequence.append('-')  # Decelerate to reduce overshooting distance
            velocity -= 1
            curr_distance -= velocity
        else:
            while velocity != 0:  # Decelerate to reach zero velocity
                optimal_sequence.append('-') if velocity > 0 else optimal_sequence.append('+')
                velocity -= 1 if velocity > 0 else velocity + 1
            
    return optimal_sequence

# Generate and print the optimal sequences for each n
for n in range(1, 22):
    optimal_sequence = generate_optimal_sequence(n)
    
    # Ensure the sequence ends with zero velocity after reaching the target distance
    if optimal_sequence[-1] == '+':
        optimal_sequence.append('-')
    elif optimal_sequence[-1] == '-':
        optimal_sequence.append('+')
        
    sequence_str = ' '.join(optimal_sequence)
    print(f"M({n}, 0) = {n}, 0, Optimal sequence: [{sequence_str}]")
