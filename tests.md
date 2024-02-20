This document outlines the non-automated tests to be performed for the Analysis package.

1. **API Token Loading Test**
    - Manually verify that the API token configuration file (`job_file.yml`) is loaded correctly.
    - Check for errors or inconsistencies in the token file.
    - Ensure that the client ID and client secret are properly configured and accessible.

2. **User Configuration Loading Test**
    - Manually verify that the user configuration file (`user_config.yml`) is loaded correctly.
    - Check for errors or inconsistencies in the user configuration.
    - Ensure that user preferences, genre choices, country names, and artist lists are properly configured.

3. **Access Token Retrieval Test**
    - Manually run the `get_access_token` method and verify that an access token is successfully retrieved.
    - Check for errors in the authentication process.
    - Ensure that the access token is valid and not expired.


4. **Data Analysis Test**
    - Manually run the `compute_analysis` method and verify that analysis metrics are computed correctly.
    - Check for errors in the analysis process.
    - Ensure that analysis results are consistent with expectations.

5. **Plotting Test**
    - Manually run the `plot_data` method and verify that a scatter plot is generated.
    - Check for errors in the plotting process.
    - Ensure that the plot is visually consistent and accurately reflects the data.

6. **Notification Test**
    - Manually run the `notify_done` method with a sample message and verify that the notification is printed.
    - Check for errors in the notification process.
    - Ensure that the message is properly displayed.