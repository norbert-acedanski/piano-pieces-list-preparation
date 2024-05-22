# -*- coding: iso-8859-15

from __future__ import annotations

import random
from typing import List, Dict, Union, Optional, Tuple, Set

from sorting_enum_class import by

PIANO_LIST_OF_PIECES = List[Dict[str, Union[str, Dict[str, Union[str, List[str], int]], List[str]]]]
STRING_OR_ITERABLE = Optional[Union[str, List[str], Tuple[str], Set[str]]]
INT_OR_ITERABLE = Optional[Union[int, List[int], Tuple[int], Set[int]]]


class PianoList:
    def __init__(self, piano_list: PIANO_LIST_OF_PIECES):
        self._piano_list = piano_list
        self.composers = sorted(self.get_all_composers())
        self.titles = sorted(self.get_all_titles())
        self.tags = sorted(self.get_all_tags())
        self.total_duration = self.get_total_duration()
        self.number_of_pieces = len(self._piano_list)

    def get_all_composers(self) -> List[str]:
        return list(set(piece["composer/performer"] for piece in self._piano_list))

    def get_all_titles(self) -> List[str]:
        return [piece["title"] for piece in self._piano_list]

    def get_all_tags(self) -> List[str]:
        tags = []
        for piece in self._piano_list:
            tags.extend(piece["tags"])
        return list(set(tags))

    def get_total_duration(self) -> int:
        return sum(piece["duration"]["minutes"]*60 + piece["duration"]["seconds"] for piece in self._piano_list)

    def get_pieces(self, from_composers: Optional[STRING_OR_ITERABLE] = None,
                         without_composers: Optional[STRING_OR_ITERABLE] = None,
                         with_titles: Optional[STRING_OR_ITERABLE] = None,
                         without_titles: Optional[STRING_OR_ITERABLE] = None,
                         longer_than: Optional[Union[int, float]] = None,
                         shorter_than: Optional[Union[int, float]] = None,
                         with_tags_and_tags: Optional[STRING_OR_ITERABLE] = None,
                         with_tags_or_tags: Optional[STRING_OR_ITERABLE] = None,
                         without_tags: Optional[STRING_OR_ITERABLE] = None,
                         with_difficulty: Optional[INT_OR_ITERABLE] = None) -> PianoList:
        if all(parameter is None for parameter in [from_composers, without_composers, with_titles, without_titles,
                                                   longer_than, shorter_than, with_tags_and_tags, with_tags_or_tags,
                                                   without_tags, with_difficulty]):
            raise ValueError("Provide at least one argument!")
        reduced_list_of_pieces = [piece for piece in self._piano_list]  # To copy the list
        if from_composers is not None:
            reduced_list_of_pieces = self._filter_composers(list_of_pieces=reduced_list_of_pieces,
                                                            composers=from_composers)
        if without_composers is not None:
            reduced_list_of_pieces = self._filter_composers(list_of_pieces=reduced_list_of_pieces,
                                                            composers=without_composers, without=True)
        if with_titles is not None:
            reduced_list_of_pieces = self._filter_titles(list_of_pieces=reduced_list_of_pieces,
                                                         titles=with_titles)
        if without_titles is not None:
            reduced_list_of_pieces = self._filter_titles(list_of_pieces=reduced_list_of_pieces,
                                                         titles=without_titles, without=True)
        if longer_than is not None:
            reduced_list_of_pieces = self._get_longer_than(list_of_pieces=reduced_list_of_pieces, duration=longer_than)
        if shorter_than is not None:
            reduced_list_of_pieces = self._get_shorter_than(list_of_pieces=reduced_list_of_pieces, duration=shorter_than)
        if with_tags_and_tags is not None:
            reduced_list_of_pieces = self._filter_and_tags(list_of_pieces=reduced_list_of_pieces, tags=with_tags_and_tags)
        if with_tags_or_tags is not None:
            reduced_list_of_pieces = self._filter_or_tags(list_of_pieces=reduced_list_of_pieces, tags=with_tags_or_tags)
        if without_tags is not None:
            reduced_list_of_pieces = self._filter_or_tags(list_of_pieces=reduced_list_of_pieces, tags=without_tags,
                                                          without=True)
        if with_difficulty is not None:
            reduced_list_of_pieces = self._filter_difficulty(list_of_pieces=reduced_list_of_pieces, difficulty=with_difficulty)
        return PianoList(reduced_list_of_pieces)

    def _filter_composers(self, list_of_pieces: PIANO_LIST_OF_PIECES, composers: STRING_OR_ITERABLE,
                          without: bool = False) -> PIANO_LIST_OF_PIECES:
        composers = [composers] if isinstance(composers, str) else composers
        if without:
            return [piece for piece in list_of_pieces if piece["composer/performer"] not in composers]
        return [piece for piece in list_of_pieces if piece["composer/performer"] in composers]

    def _filter_titles(self, list_of_pieces: PIANO_LIST_OF_PIECES, titles: STRING_OR_ITERABLE,
                       without: bool = False) -> PIANO_LIST_OF_PIECES:
        titles = [titles] if isinstance(titles, str) else titles
        if without:
            return [piece for piece in list_of_pieces if piece["title"] not in titles]
        return [piece for piece in list_of_pieces if piece["title"] in titles]

    def _get_longer_than(self, list_of_pieces: PIANO_LIST_OF_PIECES, duration: Union[int, float]) -> PIANO_LIST_OF_PIECES:
        return [piece for piece in list_of_pieces
                if piece["duration"]["minutes"]*60 + piece["duration"]["seconds"] >= duration*60]

    def _get_shorter_than(self, list_of_pieces: PIANO_LIST_OF_PIECES, duration: Union[int, float]) -> PIANO_LIST_OF_PIECES:
        return [piece for piece in list_of_pieces
                if piece["duration"]["minutes"]*60 + piece["duration"]["seconds"] <= duration*60]

    def _filter_or_tags(self, list_of_pieces: PIANO_LIST_OF_PIECES, tags: STRING_OR_ITERABLE,
                        without: bool = False) -> PIANO_LIST_OF_PIECES:
        tags = [tags] if isinstance(tags, str) else tags
        if not without:
            return [piece for piece in list_of_pieces if set(piece["tags"]) & set(tags)]
        return [piece for piece in list_of_pieces if not set(piece["tags"]) & set(tags)]

    def _filter_and_tags(self, list_of_pieces: PIANO_LIST_OF_PIECES, tags: STRING_OR_ITERABLE)\
            -> PIANO_LIST_OF_PIECES:
        tags = [tags] if isinstance(tags, str) else tags
        return [piece for piece in list_of_pieces if set(tags).issubset(set(piece["tags"]))]
    
    def _filter_difficulty(self, list_of_pieces: PIANO_LIST_OF_PIECES, difficulty: INT_OR_ITERABLE) \
            -> PIANO_LIST_OF_PIECES:
        difficulty = [difficulty] if isinstance(difficulty, int) else difficulty
        return [piece for piece in list_of_pieces if piece["difficulty"] in difficulty]

    def select_random_subgroup_based_on_duration(self, minimum_duration: Union[int, float]) -> PianoList:
        if minimum_duration < 0:
            raise ValueError("Expected duration must be positive!")
        if minimum_duration*60 > self.total_duration - 120:
            raise ValueError(f"Expected duration ({minimum_duration*60}s) bigger, than the total duration of "
                             f"all pieces ({self.total_duration - 120}s)")
        current_duration = 0
        random_pieces_list = []
        while current_duration < minimum_duration*60:
            random_piece = random.choice(self._piano_list)
            if random_piece not in random_pieces_list:
                random_pieces_list.append(random_piece)
                current_duration += random_piece["duration"]["minutes"]*60 + random_piece["duration"]["seconds"]
        return PianoList(random_pieces_list)

    def select_random_subgroup_based_on_length(self, length: int = None) -> PianoList:
        length = self.number_of_pieces if length is None else length
        if length < 0:
            raise ValueError("Expected length must be positive!")
        if length > self.number_of_pieces:
            raise ValueError(f"Expected length ({length}) bigger, than the total number of "
                             f"all pieces ({self.number_of_pieces})")
        return PianoList(random.sample(self._piano_list, k=length))

    def print_all_composers_performers(self) -> None:
        print("\nAll composers/performers:")
        for composer_number, composer in enumerate(self.composers, 1):
            print(f"{composer_number}. {composer}")

    def print_all_titles(self) -> None:
        print("\nAll titles:")
        for title_number, title in enumerate(self.titles, 1):
            print(f"{title_number}. {title}")

    def print_all_tags(self) -> None:
        print("\nAll tags:")
        for tag_number, tag in enumerate(self.tags, 1):
            print(f"{tag_number}. {tag}")

    def print_list_of_pieces(self, title: str = None, sort: by = None, reverse: bool = False,
                             print_difficulty: bool = False) -> None:
        performer_composer_str = "PERFORMER/COMPOSER"
        title_str = "TITLE"
        duration_str = "DURATION"
        performer_composer_just_length = len(max([*self.composers, performer_composer_str], key=len))
        title_just_length = len(max([*self.titles, title_str], key=len))
        list_of_pieces = self._piano_list if sort is None else self._sort_by(self._piano_list, by_what=sort, reverse=reverse)
        print("")
        if title is not None:
            print(f"{title}:")
        print(f"NR| {performer_composer_str.ljust(performer_composer_just_length)} | "
              f"{title_str.ljust(title_just_length)} | {duration_str}" + (" | DIFFICULTY" if print_difficulty else ""))
        print("-"*(performer_composer_just_length + title_just_length + len(duration_str) + 10 + (13 if print_difficulty else 0)))
        for piece_number, piece in enumerate(list_of_pieces, 1):
            print(f"{str(piece_number).rjust(2)}| "
                  f"{piece['composer/performer'].ljust(performer_composer_just_length)} | "
                  f"{piece['title'].ljust(title_just_length)} | " +
                  f"{piece['duration']['minutes']}:{str(piece['duration']['seconds']).rjust(2, '0').ljust(6)}" +
                  (f" | {piece['difficulty']}" if print_difficulty else ""))
        duration = f"{self.total_duration//60 - self.total_duration//3600*60}m {self.total_duration%60}s"
        print(f"Total duration: {(f"{self.total_duration//3600}h " if self.total_duration//3600 else "") + duration}")

    def _sort_by(self, list_of_pieces: PIANO_LIST_OF_PIECES, by_what: by, reverse: bool = False) -> PIANO_LIST_OF_PIECES:
        if by_what == by.TITLE:
            return sorted(list_of_pieces, key=lambda element: element["title"], reverse=reverse)
        elif by_what == by.COMPOSER_PERFORMER:
            return sorted(list_of_pieces, key=lambda element: element["composer/performer"], reverse=reverse)
        elif by_what == by.DURATION:
            return sorted(list_of_pieces, key=lambda element: element["duration"]["minutes"]*60 +
                                                              element["duration"]["seconds"], reverse=reverse)
        else:
            raise ValueError(f"Unexpected value '{by_what}'!")
