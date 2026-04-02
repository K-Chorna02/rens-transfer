def validate_df(df, dataset_type):
    if df.empty:
        return False, "The uploaded file is empty."

    actual_columns = [str(col).strip() for col in df.columns]
    actual_columns_set = set(actual_columns)

    required_columns = {
        'activities': [
            'Date',
            'TIme',
            'Hours',
            'Organisation',
            'Description',
            'Regularity',
            'Activity Type',
            'Access',
            'Workstreams',
            'Scale',
            'Engagement',
            'Output',
            'Attendance',
            'Location'
        ],
        'organisations': [
            'Organisation',
            'Type',
            'Focus',
            'Area of Operation',
            'TtoR',
            'Variety',
            'Regularity',
            'EQ',
            'RJ',
            'CU',
            'CJ',
            'SO',
            'SJ',
            'CE',
            'SC'
        ],
        'meetings': []
    }

    expected_columns = required_columns.get(dataset_type)

    if expected_columns is None:
        return False, f"Unknown dataset type: {dataset_type}"

    expected_columns_set = set(expected_columns)

    missing_columns = [col for col in expected_columns if col not in actual_columns_set]
    unexpected_columns = [col for col in actual_columns if col not in expected_columns_set]

    if missing_columns or unexpected_columns:
        parts = [f"Invalid columns for '{dataset_type}'."]
        parts.append(f"Required columns: {', '.join(expected_columns)}.")
        parts.append(f"Uploaded columns: {', '.join(actual_columns)}.")

        if missing_columns:
            parts.append(f"Missing columns: {', '.join(missing_columns)}.")
        if unexpected_columns:
            parts.append(f"Unexpected columns: {', '.join(unexpected_columns)}.")

        return False, " ".join(parts)

    return True, None