document.addEventListener('DOMContentLoaded', function () {
    initPanelEditing();
    initInlineEditing();
    initDeleteModal();
    initAddItemForms();
    initPillToggles();
    initRandomizerSlider();
    initLiveSearch();
});

function initPanelEditing() {
    var panels = document.querySelectorAll('.panel');
    if (!panels.length) return;

    panels.forEach(function (panel) {
        var lastTouchEnd = 0;

        panel.addEventListener('dblclick', function (e) {
            if (e.target.closest('.panel-item, form, button, input, select')) return;
            e.stopPropagation();
            togglePanelEdit(panel);
        });

        panel.addEventListener('touchend', function (e) {
            var now = Date.now();
            if (now - lastTouchEnd < 300) {
                e.preventDefault();
                e.stopPropagation();
                togglePanelEdit(panel);
            }
            lastTouchEnd = now;
        });
    });

    document.addEventListener('click', function (e) {
        document.querySelectorAll('.panel.editing').forEach(function (panel) {
            if (!e.target.closest('.panel')) {
                panel.classList.remove('editing');
            }
        });
    });
}

function initInlineEditing() {
    var heading = document.querySelector('.restaurant-heading');
    if (heading) {
        var title = heading.querySelector('.restaurant-title');
        var form = heading.querySelector('.restaurant-edit-form');
        title.addEventListener('dblclick', function () {
            heading.classList.add('is-editing');
            var input = form.querySelector('input[name="name"]');
            input.focus();
            input.select();
        });
    }

    document.querySelectorAll('.panel-item').forEach(function (item) {
        var name = item.querySelector('.panel-item-name');
        var form = item.querySelector('.food-item-edit-form');
        name.addEventListener('dblclick', function (e) {
            e.stopPropagation();
            item.classList.add('is-editing');
            var input = form.querySelector('input[name="name"]');
            input.focus();
            input.select();
        });
    });

    document.querySelectorAll('.cancel-edit').forEach(function (button) {
        button.addEventListener('click', function () {
            var container = button.closest('.restaurant-heading, .panel-item');
            if (container) {
                var form = container.querySelector('form');
                if (form) form.reset();
                container.classList.remove('is-editing');
            }
        });
    });
}

function togglePanelEdit(panel) {
    var wasEditing = panel.classList.contains('editing');
    document.querySelectorAll('.panel.editing').forEach(function (p) {
        p.classList.remove('editing');
    });
    if (!wasEditing) {
        panel.classList.add('editing');
    }
}

function initDeleteModal() {
    var modal = document.getElementById('delete-modal');
    var panelsContainer = document.querySelector('.panels');
    if (!modal || !panelsContainer) return;

    var urlTemplate = panelsContainer.dataset.deleteUrlTemplate;
    var textEl = document.getElementById('delete-modal-text');
    var form = document.getElementById('delete-modal-form');
    var noBtn = document.getElementById('delete-modal-no');

    function closeModal() {
        modal.classList.remove('open');
    }

    // Delegated so it also catches delete-dots added later by initAddItemForms.
    panelsContainer.addEventListener('click', function (e) {
        var btn = e.target.closest('.delete-dot');
        if (!btn) return;
        e.stopPropagation();
        var name = btn.dataset.itemName;
        var itemId = btn.dataset.itemId;
        textEl.textContent = 'Are you sure you want to delete "' + name + '"?';
        form.action = urlTemplate.replace('/0/', '/' + itemId + '/');
        modal.classList.add('open');
    });

    noBtn.addEventListener('click', closeModal);

    modal.addEventListener('click', function (e) {
        if (e.target === modal) closeModal();
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('open')) closeModal();
    });
}

function initAddItemForms() {
    document.querySelectorAll('.add-item-form').forEach(function (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var input = form.querySelector('.add-item-input');
            var name = input.value.trim();
            if (!name) return;

            fetch(form.action, {
                method: 'POST',
                headers: {'X-Requested-With': 'XMLHttpRequest'},
                credentials: 'same-origin',
                body: new FormData(form),
            })
                .then(function (resp) { return resp.ok ? resp.json() : null; })
                .then(function (data) {
                    if (!data) return;
                    window.location.reload();
                });
        });
    });
}

function initPillToggles() {
    document.querySelectorAll('.pill-toggle').forEach(function (toggle) {
        var hiddenInput = document.getElementById(toggle.dataset.input);
        var options = Array.prototype.slice.call(toggle.querySelectorAll('.pill-toggle-option'));

        options.forEach(function (opt, index) {
            opt.addEventListener('click', function () {
                if (opt.classList.contains('active')) return;
                options.forEach(function (o) { o.classList.remove('active'); });
                opt.classList.add('active');
                toggle.classList.toggle('is-second', index === 1);
                if (hiddenInput) {
                    hiddenInput.value = opt.dataset.value;
                    hiddenInput.dispatchEvent(new Event('change', {bubbles: true}));
                }
            });
        });
    });
}

function initRandomizerSlider() {
    var rangeInput = document.getElementById('daypart-range');
    if (!rangeInput) return;

    var dayparts = ['morning', 'afternoon', 'evening'];
    var hiddenInput = document.getElementById('daypart-input');
    var labels = document.querySelectorAll('.slider-labels span');
    var max = Number(rangeInput.max) || dayparts.length - 1;

    var updateDaypart = function () {
        var value = dayparts[rangeInput.value];
        hiddenInput.value = value;
        labels.forEach(function (label) {
            label.classList.toggle('active', label.dataset.value === value);
        });
        rangeInput.style.setProperty('--fill', (rangeInput.value / max * 100) + '%');
    };
    rangeInput.addEventListener('input', updateDaypart);
    updateDaypart();
}

function initLiveSearch() {
    var form = document.querySelector('.search-form');
    var input = document.querySelector('.search-input');
    var resultsContainer = document.getElementById('search-results');
    if (!form || !input || !resultsContainer) return;

    var modeInput = form.querySelector('input[name="mode"]');
    var debounceTimer = null;

    function runSearch() {
        var params = new URLSearchParams({mode: modeInput.value, q: input.value});
        input.placeholder = 'Search ' + modeInput.value + '...';
        fetch(window.location.pathname + '?' + params.toString(), {
            headers: {'X-Requested-With': 'XMLHttpRequest'},
            credentials: 'same-origin',
        })
            .then(function (resp) { return resp.text(); })
            .then(function (html) {
                resultsContainer.innerHTML = html;
            });
    }

    input.addEventListener('input', function () {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(runSearch, 200);
    });

    modeInput.addEventListener('change', function () {
        clearTimeout(debounceTimer);
        runSearch();
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        clearTimeout(debounceTimer);
        runSearch();
    });
}
