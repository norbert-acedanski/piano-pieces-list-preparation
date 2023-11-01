from piano_list_class import PianoList
from read_json import read_json
from sorting_enum_class import by

if __name__ == "__main__":
    piano_pieces = read_json("piano_pieces.json")
    original_piece_list = PianoList(piano_pieces)
    original_piece_list.print_all_composers_performers()
    original_piece_list.print_all_titles()
    original_piece_list.print_all_tags()
    original_piece_list.print_list_of_pieces(title="All pieces")

    duration = {"hours": 2, "minutes": 40}
    pieces_based_on_duration = original_piece_list.get_pieces(without_tags=["not good enough", "christmas"])
    pieces_based_on_duration.select_random_subgroup_based_on_duration(minimum_duration=duration["hours"]*60 +
                                                                                       duration["minutes"]).\
        print_list_of_pieces(title=f"Pieces for {duration['hours']}h {duration['minutes']}m")

    pieces_based_on_duration.select_random_subgroup_based_on_length().print_list_of_pieces("Pieces for max duration")

    soundtracks = original_piece_list.get_pieces(with_tags_and_tags="soundtrack", without_tags="not good enough")
    soundtracks.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title="Soundtracks")

    classical = original_piece_list.get_pieces(with_tags_and_tags="classical", without_tags="not good enough")
    classical.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title="Classical")

    energetic = original_piece_list.get_pieces(with_tags_and_tags="energetic")
    energetic.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title="Energetic")

    songs_sorted_duration = original_piece_list.get_pieces(with_tags_and_tags="song")
    songs_sorted_duration.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title="Songs sorted by duration", sort=by.DURATION)

    christmas_songs = original_piece_list.get_pieces(with_tags_and_tags="christmas")
    christmas_songs.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title="Christmas songs")

    for_children = original_piece_list.get_pieces(with_tags_and_tags="for children")
    for_children.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title="For children")

    for_children_and_christmas = original_piece_list.get_pieces(with_tags_or_tags=["for children", "christmas"])
    for_children_and_christmas.select_random_subgroup_based_on_length().\
        print_list_of_pieces("For children and christmas", sort=by.TITLE)

    happy_songs = original_piece_list.get_pieces(with_tags_and_tags="happy")
    happy_songs.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title="Happy songs")

    energetic_or_for_children_or_happy_songs = original_piece_list.get_pieces(
        with_tags_or_tags=["energetic", "for children", "happy"], without_tags="christmas")
    energetic_or_for_children_or_happy_songs.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title="Energetic, for children or happy songs")

    sad_pieces_sorted_title = original_piece_list.get_pieces(with_tags_and_tags="sad", without_tags="not good enough")
    sad_pieces_sorted_title.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title="Sad pieces sorted by title reversed", sort=by.TITLE, reverse=True)

    not_good_enough_pieces = original_piece_list.get_pieces(with_tags_and_tags="not good enough")
    not_good_enough_pieces.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title="Not good enough pieces")

    pieces_to_practice_weekly = original_piece_list.get_pieces(with_tags_or_tags=["christmas", "not good enough",
                                                                                  "fresh"])
    pieces_to_practice_weekly.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title="Pieces to practice weekly", sort=by.COMPOSER_PERFORMER)

    old_flat_left_pieces = [piece for piece in original_piece_list._piano_list
                            if set(piece["channel state"].get("old flat", {})) == {"recorded"}]
    pieces_from_old_flat_left_to_upload = PianoList(old_flat_left_pieces)
    pieces_from_old_flat_left_to_upload.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title="Pieces left to upload from the old flat")
