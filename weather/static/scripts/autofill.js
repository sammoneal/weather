const form = document.getElementById("form");
const locationInput = document.getElementById("location");
const dropdown = document.getElementById("dropdown");

locationInput.addEventListener("input", generateAutofill);
locationInput.addEventListener("focus", generateAutofill);
locationInput.addEventListener("focusout", loseFocus);

function generateAutofill(event) {
  const input = event.target;
  if (!input.value) {
    dropdown.style.display = "none";
    return;
  }
  dropdown.style.display = "block";
  const results = search(input.value);
  if (!results) {
    dropdown.style.display = "none";
    return
  }
  dropdown.innerHTML = results;
  const entries = document.getElementsByClassName("dropdown-entry");
  for (let i = 0; i < entries.length; i++) {
    const element = entries[i];
    element.addEventListener("click", (event) => {
      input.value = element.textContent;
      form.submit();
    });
  }
}

function loseFocus(event) {
  const input = event.target;
  if (!input.value) {
    dropdown.style.display = "none";
    return;
  }
}

function search(text) {
  let results = [];
  for (const property in cityData) {
    // State level match
    const stateIndex = property.toLowerCase().indexOf(text.toLowerCase());
    if (stateIndex > -1) {
      for (const item of cityData[property]) {
        results.push([
          `<p class="dropdown-entry">${item}, ${emSlice(
            property,
            stateIndex,
            text.length
          )}</p>`,
          stateIndex * 10,
        ]);
      }
    }
    // City level match
    for (const item of cityData[property]) {
      const cityIndex = item.toLowerCase().indexOf(text.toLowerCase());
      if (cityIndex > -1) {
        results.push([
          `<p class="dropdown-entry">${emSlice(
            item,
            cityIndex,
            text.length
          )}, ${property}</p>`,
          cityIndex,
        ]);
      }
    }
  }
  results.sort((a, b) => a[1] - b[1]);
  results = results.slice(0, 6);
  for (let i = 0; i < results.length; i++) {
    results[i].pop();
  }
  return results.join("");
}

function emSlice(text, index, emLength) {
  let sliced = "";
  const emEnd = index + emLength;
  if (index > 0) {
    sliced += text.slice(0, index);
  }
  sliced += '<span class="match">';
  sliced += text.slice(index, emEnd);
  sliced += "</span>";
  if (text.length > emEnd) {
    sliced += text.slice(emEnd, text.length);
  }
  return sliced;
}