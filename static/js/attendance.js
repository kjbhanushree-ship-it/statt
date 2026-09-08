/* BIT Attendance System — attendance.js */

document.addEventListener('DOMContentLoaded', function () {

  // ── Auto-dismiss alerts after 4 seconds ─────────────────────────────────
  document.querySelectorAll('.alert.alert-success, .alert.alert-info').forEach(function (el) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
      if (bsAlert) bsAlert.close();
    }, 4000);
  });

  // ── Confirm on form submits that are destructive ─────────────────────────
  document.querySelectorAll('[data-confirm]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (!confirm(this.dataset.confirm)) e.preventDefault();
    });
  });

  // ── Attendance count tracker on mark page ───────────────────────────────
  const countPresent  = document.getElementById('countPresent');
  const countAbsent   = document.getElementById('countAbsent');
  const countLate     = document.getElementById('countLate');

  function updateCounts() {
    if (!countPresent) return;
    let p = 0, a = 0, l = 0;
    document.querySelectorAll('input[type=radio]:checked').forEach(function (r) {
      if (r.value === 'P') p++;
      else if (r.value === 'A') a++;
      else if (r.value === 'L') l++;
    });
    countPresent.textContent = p;
    countAbsent.textContent  = a;
    countLate.textContent    = l;
  }

  document.querySelectorAll('input[type=radio]').forEach(function (r) {
    r.addEventListener('change', updateCounts);
  });
  updateCounts();

  // ── Dynamic subject filter via API ───────────────────────────────────────
  const deptSel    = document.getElementById('deptFilter');
  const semSel     = document.getElementById('semFilter');
  const subjectSel = document.getElementById('subjectFilter');

  function loadSubjects() {
    if (!subjectSel) return;
    const dept = deptSel ? deptSel.value : '';
    const sem  = semSel  ? semSel.value  : '';
    let url = '/api/subjects?';
    if (dept) url += 'dept_id=' + dept + '&';
    if (sem)  url += 'semester=' + sem;
    fetch(url)
      .then(r => r.json())
      .then(function (data) {
        const cur = subjectSel.value;
        subjectSel.innerHTML = '<option value="">-- Select Subject --</option>';
        data.forEach(function (s) {
          const opt = document.createElement('option');
          opt.value = s.id;
          opt.textContent = s.code + ' — ' + s.name + ' (Sec ' + s.section + ')';
          if (s.id == cur) opt.selected = true;
          subjectSel.appendChild(opt);
        });
      })
      .catch(console.error);
  }

  if (deptSel)   deptSel.addEventListener('change', loadSubjects);
  if (semSel)    semSel.addEventListener('change',  loadSubjects);

  // ── Tooltip init ─────────────────────────────────────────────────────────
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
    bootstrap.Tooltip.getOrCreateInstance(el);
  });
});
