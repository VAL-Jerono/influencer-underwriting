# Data dictionary (Phase 0)

## post_info.txt (tab-separated, no header)
| column | status |
|---|---|
| post_id | assumed unique id; audit reports duplicates |
| username | creator handle |
| sponsored | label; encoding to be confirmed (config `positive_labels`) |
| json_file | JSON filename inside json_files.zip |
| image_files | image filenames; separator to be confirmed (config `image_sep`) |

Every cleaning decision made later must be recorded here.
