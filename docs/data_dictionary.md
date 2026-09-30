# Data dictionary (Phase 0)

- Kim et al. Instagram Influencer Dataset (WWW 2020) 

- 33,935 real Instagram influencer entities, 10,180,500 posts, post JSON, captions, images, and nine-category landing-page labels.

- Request form with affiliation, email, research/education use, and copyright/license agreement.

- Historical Instagram snapshot, very large local storage requirement, and category-label discrepancies between the landing page and paper.





## post_info.txt (tab-separated, no header)
| column | status |
|---|---|
| post_id | assumed unique id; audit reports duplicates |
| username | creator handle |
| sponsored | label; encoding to be confirmed (config `positive_labels`) |
| json_file | JSON filename inside json_files.zip |
| image_files | image filenames; separator to be confirmed (config `image_sep`) |

Every cleaning decision made later must be recorded here.
