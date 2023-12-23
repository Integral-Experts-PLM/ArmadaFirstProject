  document.addEventListener('DOMContentLoaded', function () {
    const projectIdSelect = document.getElementById('project_id');
    const systemIdSelect = document.getElementById('system_id');
    const configurationIdSelect = document.getElementById('configuration_id');
    const configurationNameSelect = document.getElementById('configuration_name');
    const treeItemIdSelect = document.getElementById('tree_item_id');
    const treeItemNameSelect = document.getElementById('tree_item_name');

    if (projectIdSelect) {
      projectIdSelect.addEventListener('change', handleProjectChange);
      systemIdSelect.addEventListener('change', handleSystemChange);
      configurationIdSelect.addEventListener('change', handleConfigurationChange);
    //   treeItemIdSelect.addEventListener('change', checkFormAndSubmit);
      projectIdSelect.addEventListener('change', function () {
        const selectedProjectName = projectIdSelect.options[projectIdSelect.selectedIndex].text;
        document.getElementById('project_name').value = selectedProjectName;
      });
      systemIdSelect.addEventListener('change', function () {
        const selectedSystemName = systemIdSelect.options[systemIdSelect.selectedIndex].text;
        document.getElementById('system_name').value = selectedSystemName;
      });
    }

    // function checkFormAndSubmit() {
    //   const selectedItemName = treeItemIdSelect.options[treeItemIdSelect.selectedIndex].text;
    //   if(selectedItemName != 'All Items') {
    //     treeItemNameSelect.value = selectedItemName;
    //   } else {
    //     treeItemNameSelect.value = null;
    //   }

    //   if (projectIdSelect.value && systemIdSelect.value && configurationIdSelect.value && treeItemIdSelect.value) {
    //     document.getElementById('incident-form').submit();
    //   }
    // }

    // Function to get the CSRF token from cookies
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === name + '=') {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }

    function handleProjectChange() {
    //   messageContainer.textContent = '';
      let selectedProjectId = projectIdSelect.value;

      // Send the selectedProjectId as a string to your Django view using an AJAX request
      fetch('/get-systems/', {
        method: 'POST',
        headers: {
          'Content-Type': 'text/plain',
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: selectedProjectId,
      })
        .then(handleResponse)
        .then(data => {
          systemIdSelect.removeAttribute('disabled');
          populateDropdown(systemIdSelect, data.allSystemsFromProject, "Name");
        })
        .catch(handleError);
    }

    function handleSystemChange() {
    //   messageContainer.textContent = '';
      let selectedProjectId = projectIdSelect.value;
      let selectedSystemtId = systemIdSelect.value;
      let requestBody = {
        projectId: selectedProjectId,
        systemId: selectedSystemtId
      };
      let requestBodyJSON = JSON.stringify(requestBody);

      // Send the selectedProjectId as a string to your Django view using an AJAX request
      fetch('/get-configurations/', {
        method: 'POST',
        headers: {
          'Content-Type': 'text/plain',
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: requestBodyJSON,
      })
        .then(handleResponse)
        .then(data => {
          configurationIdSelect.removeAttribute('disabled');
          populateDropdown(configurationIdSelect, data.allConfigurationsFromProjectAndSystem, "Name");
        })
        .catch(handleError);
    }

    function handleConfigurationChange() {
      const selectedProjectId = projectIdSelect.value;
      const selectedSystemtId = systemIdSelect.value;
      const selectedConfigurationId = configurationIdSelect.value;
      const selectedConfigurationName = configurationIdSelect.options[configurationIdSelect.selectedIndex].text;
      configurationNameSelect.value = selectedConfigurationName;
      const requestBody = {
        projectId: selectedProjectId,
        systemId: selectedSystemtId,
        configurationId: selectedConfigurationId,
      };
      let requestBodyJSON = JSON.stringify(requestBody);
      // Send the selectedProjectId as a string to your Django view using an AJAX request
      fetch('/get-tree-items/', {
        method: 'POST',
        headers: {
          'Content-Type': 'text/plain',
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: requestBodyJSON,
      })
        .then(handleResponse)
        .then(data => {
          // if (data.allTreeItemsFromProjectSystemConfiguration == null) {
          //   messageContainer.textContent = 'No Items for this combination!';
          // } else
          {
            treeItemIdSelect.removeAttribute('disabled');
            populateDropdown(treeItemIdSelect, data.allTreeItemsFromProjectSystemConfiguration, "Name");
          }
        })
        .catch(handleError);
    }

    function handleResponse(response) {
      if (!response.ok) {
        throw new Error('Request failed');
      }
      return response.json();
    }

    function handleError(error) {
      console.error('Error:', error);
    }

    function populateDropdown(selectElement, options, selectType) {
      selectElement.innerHTML = '<option value="">Select...</option>';
      options.forEach(option => {
        let newOption = document.createElement('option');
        newOption.value = option.ID;
        newOption.text = option[selectType];
        selectElement.appendChild(newOption);
      });
    }
  });