from magenta.music import note_seq
from note_seq.protobuf import music_pb2
import random

def create_random_sequence(num_notes=16, max_pitch=84, min_pitch=60):
    # Create a NoteSequence
    note_sequence = music_pb2.NoteSequence()
    note_sequence.tempos.add(qpm=120)  # Set tempo

    # Generate random notes
    for i in range(num_notes):
        pitch = random.randint(min_pitch, max_pitch)  # Random pitch
        start_time = i * 0.5  # Start time for each note
        end_time = start_time + 0.5  # End time for each note
        velocity = random.randint(60, 100)  # Random velocity
        note_sequence.notes.add(pitch=pitch, start_time=start_time, end_time=end_time, velocity=velocity)

    note_sequence.total_time = num_notes * 0.5  # Total time of the sequence
    return note_sequence

# Create a random NoteSequence
random_sequence = create_random_sequence()

# Save to a MIDI file
note_seq.sequence_proto_to_midi_file(random_sequence, 'random_music.mid')

print("Random music saved as 'random_music.mid'.")
