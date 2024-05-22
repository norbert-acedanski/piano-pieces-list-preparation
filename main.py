from piano_list_class import PianoList
from read_json import read_json
from sorting_enum_class import by

if __name__ == "__main__":
    piano_pieces = read_json("piano_pieces.json")
    original_piece_list = PianoList(piano_pieces)
    original_piece_list.print_all_composers_performers()
    original_piece_list.print_all_titles()
    original_piece_list.print_all_tags()
    original_piece_list.select_random_subgroup_based_on_length().print_list_of_pieces(title="All pieces")

    pieces_based_on_duration = original_piece_list.get_pieces(without_tags=["not good enough", "christmas"])
    pieces_based_on_duration.select_random_subgroup_based_on_duration(minimum_duration=110).\
        print_list_of_pieces(title=f"Pieces for 1h 50m")

    pieces_based_on_duration.select_random_subgroup_based_on_duration(minimum_duration=160).\
        print_list_of_pieces(title=f"Pieces for 2h 40m")

    pieces_based_on_duration.select_random_subgroup_based_on_duration(minimum_duration=15).\
        print_list_of_pieces(title=f"Pieces for 15m")

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

    romantic_or_energetic_songs = original_piece_list.get_pieces(
        with_tags_or_tags="romantic", without_tags=["not good enough", "christmas"])
    romantic_or_energetic_songs.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title="Romantic songs")

    sad_pieces_sorted_title = original_piece_list.get_pieces(with_tags_and_tags="sad", without_tags="not good enough")
    sad_pieces_sorted_title.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title="Sad pieces sorted by title reversed", sort=by.TITLE, reverse=True)

    not_good_enough_pieces = original_piece_list.get_pieces(with_tags_and_tags="not good enough")
    not_good_enough_pieces.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title="Not good enough pieces", print_difficulty=True)

    pieces_to_practice_weekly = original_piece_list.get_pieces(with_tags_or_tags=["christmas", "not good enough",
                                                                                  "fresh"])
    pieces_to_practice_weekly.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title="Pieces to practice weekly", sort=by.COMPOSER_PERFORMER, print_difficulty=True)

    new_flat_left_pieces = [piece for piece in original_piece_list._piano_list
                            if set(piece["channel state"].get("new flat", [])) in [{"recorded"}, set()]]
    pieces_from_new_flat_left_to_upload = PianoList(new_flat_left_pieces)
    pieces_from_new_flat_left_to_upload.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title="Pieces left to upload from the new flat", print_difficulty=True)

    pieces_not_recorded = [piece for piece in original_piece_list._piano_list
                           if "recorded" not in set(piece["channel state"].get("old flat", []))
                           and "recorded" not in set(piece["channel state"]["new flat"])]
    pieces_not_yet_recorded = PianoList(pieces_not_recorded)
    pieces_not_yet_recorded.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title="Pieces not yet recorded", print_difficulty=True)

    fixed_difficulty_pieces = original_piece_list.get_pieces(without_tags=["christmas", "not good enough"],
                                                             with_difficulty=(difficulty := [1, 2]))
    fixed_difficulty_pieces.select_random_subgroup_based_on_length().\
        print_list_of_pieces(title=f"Pieces with {difficulty=}", print_difficulty=True)
