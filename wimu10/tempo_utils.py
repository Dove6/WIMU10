from typing import List
import muspy as mp


def timestep_to_realtime(music: mp.Music, timestep: int):
    """
    music: Music that defines beat resolution and tempos
    timestap: Timestamp to convert
    returns: Timestamp in minutes
    """
    realtime = 0
    tempos = music.tempos
    resolution = music.resolution
    # Find index of the tempo the timestamp belongs to
    index = 0
    while index < len(tempos) - 1:
        if tempos[index].time <= timestep < tempos[index + 1].time:
            break
        index += 1
    # Add time from previous tempos
    for a, b in zip(tempos[: index - 1], tempos[1:index]):
        tempo_length = b.time - a.time
        realtime += tempo_length / a.qpm
    # Add time from current tempo
    tempo = tempos[index]
    tempo_length = timestep - tempo.time
    realtime += tempo_length / tempo.qpm
    return realtime / resolution
