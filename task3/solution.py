def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_start, lesson_end = intervals["lesson"]

    pupil_intervals = []
    for i in range(0, len(intervals["pupil"]), 2):
        start = max(intervals["pupil"][i], lesson_start)
        end = min(intervals["pupil"][i + 1], lesson_end)
        if start < end:
            pupil_intervals.append((start, end))

    tutor_intervals = []
    for i in range(0, len(intervals["tutor"]), 2):
        start = max(intervals["tutor"][i], lesson_start)
        end = min(intervals["tutor"][i + 1], lesson_end)
        if start < end:
            tutor_intervals.append((start, end))

    pupil_intervals.sort()
    tutor_intervals.sort()

    def merge_intervals(intervals):
        if not intervals:
            return []
        merged = [intervals[0]]
        for current in intervals[1:]:
            prev = merged[-1]
            if current[0] <= prev[1]:
                merged[-1] = (prev[0], max(prev[1], current[1]))
            else:
                merged.append(current)
        return merged

    merged_pupil = merge_intervals(pupil_intervals)
    merged_tutor = merge_intervals(tutor_intervals)

    total_time = 0
    pupil_idx = 0
    tutor_idx = 0

    while pupil_idx < len(merged_pupil) and tutor_idx < len(merged_tutor):
        pupil_start, pupil_end = merged_pupil[pupil_idx]
        tutor_start, tutor_end = merged_tutor[tutor_idx]

        overlap_start = max(pupil_start, tutor_start)
        overlap_end = min(pupil_end, tutor_end)

        if overlap_start < overlap_end:
            total_time += overlap_end - overlap_start

        if pupil_end < tutor_end:
            pupil_idx += 1
        else:
            tutor_idx += 1

    return total_time
