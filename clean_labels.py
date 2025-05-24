def clean_labels(labels_folder):
    classes_found_before = set()
    classes_found_after = set()

    for file in os.listdir(labels_folder):
        if file.endswith('.txt'):
            file_path = os.path.join(labels_folder, file)
            with open(file_path, 'r') as f:
                lines = f.readlines()

            cleaned_lines = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 0:
                    continue  # Skip empty lines
                try:
                    cls_id = int(parts[0])
                    classes_found_before.add(cls_id)

                    if cls_id == 0:
                        cleaned_lines.append(line)
                        classes_found_after.add(cls_id)
                except ValueError:
                    print(f"⚠️ Skipping malformed line in {file}: {line.strip()}")

            # Overwrite label file with cleaned lines
            with open(file_path, 'w') as f:
                f.writelines(cleaned_lines)

    print(f"Classes found BEFORE cleaning: {sorted(classes_found_before)}")
    print(f"Classes found AFTER cleaning: {sorted(classes_found_after)}")
    if classes_found_after == {0}:
        print("✅ All labels cleaned successfully — only class 0 remains.")
    else:
        print("⚠️ Warning: Unexpected classes remain after cleaning.")
