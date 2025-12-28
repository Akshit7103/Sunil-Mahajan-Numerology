/**
 * Numerology Calculator - Main JavaScript
 * Handles form submission, results display, and PDF export
 */

// Global variable to store the latest calculation result
let currentNumerologyData = null;

// Initialize event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeGenderButtons();
    initializeFormHandlers();
});

/**
 * Initialize gender button selection handlers
 * Fixes the issue where buttons don't glow on initial selection
 */
function initializeGenderButtons() {
    const male = document.getElementById('male');
    const female = document.getElementById('female');
    const segMale = document.getElementById('segMale');
    const segFemale = document.getElementById('segFemale');

    function syncGenderButtons() {
        segMale.classList.toggle('active', male.checked);
        segFemale.classList.toggle('active', female.checked);
    }

    male.addEventListener('change', syncGenderButtons);
    female.addEventListener('change', syncGenderButtons);

    // Initial sync on page load
    syncGenderButtons();
}

/**
 * Initialize form submission and reset handlers
 */
function initializeFormHandlers() {
    const form = document.getElementById('numerologyForm');
    const resetBtn = document.getElementById('resetBtn');

    form.addEventListener('submit', handleFormSubmit);
    resetBtn.addEventListener('click', handleFormReset);
}

/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();

    const name = document.getElementById('name').value;
    const dob = document.getElementById('dob').value;
    const genderElement = document.querySelector('input[name="gender"]:checked');

    if (!genderElement) {
        showError('Please select a gender');
        return;
    }

    const gender = genderElement.value;
    const errorDiv = document.getElementById('error');
    const resultsDiv = document.getElementById('results');

    // Clear previous errors and results
    errorDiv.classList.remove('show');
    resultsDiv.classList.remove('show');

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                date_of_birth: dob,
                gender: gender
            })
        });

        const data = await response.json();

        if (data.success) {
            currentNumerologyData = data;
            displayResults(data);
            resultsDiv.classList.add('show');
            resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('An error occurred. Please try again.');
        console.error('Error:', error);
    }
}

/**
 * Handle form reset
 */
function handleFormReset() {
    document.getElementById('numerologyForm').reset();
    document.getElementById('results').classList.remove('show');
    document.getElementById('error').classList.remove('show');

    // Re-sync gender buttons after reset
    const male = document.getElementById('male');
    const female = document.getElementById('female');
    const segMale = document.getElementById('segMale');
    const segFemale = document.getElementById('segFemale');

    segMale.classList.remove('active');
    segFemale.classList.remove('active');

    window.scrollTo({top: 0, behavior: 'smooth'});
}

/**
 * Display error message
 */
function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = 'Error: ' + message;
    errorDiv.classList.add('show');
}

/**
 * Display numerology results
 */
function displayResults(data) {
    // Update header information
    document.getElementById('resultName').textContent = data.name;
    document.getElementById('resultDob').textContent =
        `Born on ${new Date(data.date_of_birth).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        })}`;

    // Update main numbers
    document.getElementById('driverValue').textContent = data.driver;
    document.getElementById('conductorValue').textContent = data.conductor;
    document.getElementById('kuaValue').textContent = data.kua;

    // Populate Loshu Grid
    populateLoshuGrid(data.loshu_grid);

    // Populate present and missing numbers
    populatePresentNumbers(data.present_numbers);
    populateMissingNumbers(data.missing_numbers);

    // Populate compatibility sections
    populateCompatibility('driver', data.driver, data.driver_compatibility);
    populateCompatibility('conductor', data.conductor, data.conductor_compatibility);

    // Populate number summaries
    populateNumberSummaries(data.lucky_numbers, data.bad_numbers, data.neutral_numbers);

    // Populate remedies
    populateRemedies(data.remedies_part1, data.remedies_part2, data.remedies_part3);

    // Populate luck factors
    populateLuckFactors(data.luck_factors);

    // Populate name numerology analysis
    populateNameNumerology(data.name_analysis);
}

/**
 * Populate Loshu Grid
 */
function populateLoshuGrid(loshuGrid) {
    const container = document.getElementById('loshuGrid');
    container.innerHTML = '';

    loshuGrid.forEach(row => {
        row.forEach(cell => {
            const cellDiv = document.createElement('div');
            cellDiv.className = 'loshu-cell';

            if (cell.present) {
                cellDiv.classList.add('present');
            } else {
                cellDiv.classList.add('missing');
            }

            // Show base number and count badge
            const base = String(cell.value).charAt(0);
            cellDiv.textContent = base;

            if (cell.count && cell.count > 1) {
                const badge = document.createElement('span');
                badge.className = 'loshu-count';
                badge.textContent = `×${cell.count}`;
                cellDiv.appendChild(badge);
            }

            container.appendChild(cellDiv);
        });
    });
}

/**
 * Populate present numbers
 */
function populatePresentNumbers(presentNumbers) {
    const list = document.getElementById('presentNumbersList');
    list.textContent = presentNumbers.join(', ');
}

/**
 * Populate missing numbers
 */
function populateMissingNumbers(missingNumbers) {
    const container = document.getElementById('missingNumbersList');
    const section = document.getElementById('missingNumbers');

    container.innerHTML = '';

    if (missingNumbers.length > 0) {
        missingNumbers.forEach(num => {
            const badge = document.createElement('div');
            badge.className = 'missing-number-badge';
            badge.textContent = num;
            container.appendChild(badge);
        });
        section.style.display = 'block';
    } else {
        section.style.display = 'none';
    }
}

/**
 * Populate compatibility section
 */
function populateCompatibility(type, number, compatData) {
    if (!compatData) return;

    document.getElementById(`${type}NumCompat`).textContent = number;
    document.getElementById(`${type}Planet`).textContent = compatData.planet || '';

    // Friends
    const friendsDiv = document.getElementById(`${type}Friends`);
    friendsDiv.innerHTML = '';
    const friendsRaw = compatData.friends_raw || '';
    if (friendsRaw) {
        const badge = createBadge(friendsRaw, 'friends');
        friendsDiv.appendChild(badge);
    }

    // Non-friends
    const nonFriendsDiv = document.getElementById(`${type}NonFriends`);
    nonFriendsDiv.innerHTML = '';
    const nonFriendsRaw = compatData.non_friends_raw || '';
    if (nonFriendsRaw && nonFriendsRaw !== '--------') {
        const badge = createBadge(nonFriendsRaw, 'non-friends');
        nonFriendsDiv.appendChild(badge);
    } else {
        nonFriendsDiv.textContent = 'None';
        nonFriendsDiv.style.color = '#999';
    }

    // Neutral
    const neutralDiv = document.getElementById(`${type}Neutral`);
    neutralDiv.innerHTML = '';
    const neutralRaw = compatData.neutral_raw || '';
    if (neutralRaw) {
        const badge = createBadge(neutralRaw, 'neutral');
        neutralDiv.appendChild(badge);
    }
}

/**
 * Create a number badge
 */
function createBadge(text, className) {
    const badge = document.createElement('div');
    badge.className = `number-badge ${className}`;
    badge.textContent = text;
    badge.style.width = 'auto';
    badge.style.padding = '8px 12px';
    return badge;
}

/**
 * Populate number summaries (lucky, bad, neutral)
 */
function populateNumberSummaries(luckyNumbers, badNumbers, neutralNumbers) {
    populateNumberSummary('luckyNumbersSummary', luckyNumbers, 'lucky');
    populateNumberSummary('badNumbersSummary', badNumbers, 'bad');
    populateNumberSummary('neutralNumbersSummary', neutralNumbers, 'neutral-num');
}

/**
 * Populate individual number summary
 */
function populateNumberSummary(elementId, numbers, className) {
    const container = document.getElementById(elementId);
    container.innerHTML = '';

    if (numbers && numbers.length > 0) {
        numbers.forEach(num => {
            const numDiv = document.createElement('div');
            numDiv.className = `summary-number ${className}`;
            numDiv.textContent = num;
            container.appendChild(numDiv);
        });
    } else {
        container.innerHTML = '<p style="color: #999;">None</p>';
    }
}

/**
 * Populate all remedies sections
 */
function populateRemedies(part1, part2, part3) {
    populateRemediesPart1(part1);
    populateRemediesPart2(part2);
    populateRemediesPart3(part3);
}

/**
 * Populate remedies part 1
 */
function populateRemediesPart1(remedies) {
    const container = document.getElementById('remediesPart1Container');
    container.innerHTML = '';

    if (remedies && remedies.length > 0) {
        remedies.forEach(remedy => {
            const card = createRemedyCard(remedy.condition, remedy.remedy);
            container.appendChild(card);
        });
    } else {
        container.innerHTML = '<div class="no-remedies">No missing numbers! Your Loshu Grid is complete.</div>';
    }
}

/**
 * Populate remedies part 2
 */
function populateRemediesPart2(remedies) {
    const container = document.getElementById('remediesPart2Container');
    container.innerHTML = '';

    if (remedies && remedies.length > 0) {
        remedies.forEach(remedy => {
            const card = createRemedyCard(remedy.remedy, 'Condition: ' + remedy.condition);
            container.appendChild(card);
        });
    } else {
        container.innerHTML = '<div class="no-remedies">No Yantra-based remedies applicable.</div>';
    }
}

/**
 * Create remedy card element
 */
function createRemedyCard(title, text) {
    const card = document.createElement('div');
    card.className = 'remedy-card';

    const titleDiv = document.createElement('div');
    titleDiv.className = 'condition';
    titleDiv.textContent = title.startsWith('If ') ? title : 'If ' + title;

    const textDiv = document.createElement('div');
    textDiv.className = 'remedy-text';
    textDiv.textContent = text;

    card.appendChild(titleDiv);
    card.appendChild(textDiv);

    return card;
}

/**
 * Populate remedies part 3 (table format)
 */
function populateRemediesPart3(remedies) {
    const container = document.getElementById('remediesPart3Container');
    container.innerHTML = '';

    if (remedies && remedies.length > 0) {
        const table = createRemediesTable(remedies);
        container.appendChild(table);
    } else {
        container.innerHTML = '<div class="no-remedies">No missing numbers! No planet-based remedies needed.</div>';
    }
}

/**
 * Create remedies table
 */
function createRemediesTable(remedies) {
    const table = document.createElement('table');
    table.className = 'remedies-table';

    // Create header
    const thead = document.createElement('thead');
    thead.innerHTML = `
        <tr>
            <th>No.</th>
            <th>Planet</th>
            <th>Remedy / Action</th>
        </tr>
    `;
    table.appendChild(thead);

    // Create body
    const tbody = document.createElement('tbody');
    remedies.forEach(item => {
        const tr = document.createElement('tr');

        const tdNum = document.createElement('td');
        tdNum.className = 'number-col';
        tdNum.textContent = item.number;

        const tdPlanet = document.createElement('td');
        tdPlanet.className = 'planet-col';
        tdPlanet.textContent = item.planet;

        const tdRemedies = document.createElement('td');
        tdRemedies.className = 'remedy-col';

        if (item.remedies.length === 1) {
            tdRemedies.textContent = item.remedies[0];
        } else {
            const ul = document.createElement('ul');
            item.remedies.forEach(remedy => {
                const li = document.createElement('li');
                li.textContent = remedy;
                ul.appendChild(li);
            });
            tdRemedies.appendChild(ul);
        }

        tr.appendChild(tdNum);
        tr.appendChild(tdPlanet);
        tr.appendChild(tdRemedies);
        tbody.appendChild(tr);
    });
    table.appendChild(tbody);

    return table;
}

/**
 * Populate luck factors table
 */
function populateLuckFactors(luckFactors) {
    const container = document.getElementById('luckFactorContainer');
    container.innerHTML = '';

    if (luckFactors && luckFactors.length > 0) {
        const table = createLuckFactorTable(luckFactors);
        container.appendChild(table);
    }
}

/**
 * Create luck factor table
 */
function createLuckFactorTable(factors) {
    const table = document.createElement('table');
    table.className = 'luck-factor-table';

    // Create header
    const thead = document.createElement('thead');
    thead.innerHTML = `
        <tr>
            <th>Year</th>
            <th>Date</th>
            <th>PY, D</th>
            <th>Luck Factor</th>
        </tr>
    `;
    table.appendChild(thead);

    // Create body
    const tbody = document.createElement('tbody');
    factors.forEach(item => {
        const tr = document.createElement('tr');

        const tdYear = document.createElement('td');
        tdYear.className = 'year-col';
        tdYear.textContent = item.year;

        const tdDate = document.createElement('td');
        tdDate.textContent = item.date;

        const tdCombination = document.createElement('td');
        tdCombination.className = 'combination-col';
        tdCombination.textContent = item.combination;

        const tdPercentage = document.createElement('td');
        tdPercentage.className = 'percentage-col';
        tdPercentage.textContent = item.luck_factor;

        tr.appendChild(tdYear);
        tr.appendChild(tdDate);
        tr.appendChild(tdCombination);
        tr.appendChild(tdPercentage);
        tbody.appendChild(tr);
    });
    table.appendChild(tbody);

    return table;
}

/**
 * Populate name numerology analysis section
 */
function populateNameNumerology(nameAnalysis) {
    if (!nameAnalysis) return;

    // First name
    document.getElementById('firstName').textContent = nameAnalysis.first_name;
    document.getElementById('firstNameValue').textContent = nameAnalysis.first_name_value;

    // First name breakdown
    const firstBreakdown = document.getElementById('firstNameBreakdown');
    firstBreakdown.innerHTML = '';
    if (nameAnalysis.first_name_breakdown && nameAnalysis.first_name_breakdown.breakdown) {
        nameAnalysis.first_name_breakdown.breakdown.forEach(item => {
            const letterDiv = document.createElement('div');
            letterDiv.className = item.letter === ' ' ? 'letter-value space' : 'letter-value';

            if (item.letter !== ' ') {
                const letterSpan = document.createElement('div');
                letterSpan.className = 'letter';
                letterSpan.textContent = item.letter;

                const valueSpan = document.createElement('div');
                valueSpan.className = 'value';
                valueSpan.textContent = item.value;

                letterDiv.appendChild(letterSpan);
                letterDiv.appendChild(valueSpan);
            } else {
                letterDiv.textContent = '•';
            }

            firstBreakdown.appendChild(letterDiv);
        });
    }

    // Full name
    document.getElementById('fullNameDisplay').textContent = nameAnalysis.full_name;
    document.getElementById('fullNameValue').textContent = nameAnalysis.full_name_value;

    // Full name breakdown
    const fullBreakdown = document.getElementById('fullNameBreakdown');
    fullBreakdown.innerHTML = '';
    if (nameAnalysis.full_name_breakdown && nameAnalysis.full_name_breakdown.breakdown) {
        nameAnalysis.full_name_breakdown.breakdown.forEach(item => {
            const letterDiv = document.createElement('div');
            letterDiv.className = item.letter === ' ' ? 'letter-value space' : 'letter-value';

            if (item.letter !== ' ') {
                const letterSpan = document.createElement('div');
                letterSpan.className = 'letter';
                letterSpan.textContent = item.letter;

                const valueSpan = document.createElement('div');
                valueSpan.className = 'value';
                valueSpan.textContent = item.value;

                letterDiv.appendChild(letterSpan);
                letterDiv.appendChild(valueSpan);
            } else {
                letterDiv.textContent = '•';
            }

            fullBreakdown.appendChild(letterDiv);
        });
    }

    // Followed rules
    const followedRulesContainer = document.getElementById('followedRules');
    followedRulesContainer.innerHTML = '';

    if (nameAnalysis.followed_rules && nameAnalysis.followed_rules.length > 0) {
        nameAnalysis.followed_rules.forEach(rule => {
            const ruleDiv = document.createElement('div');
            ruleDiv.className = `rule-item ${rule.status}`;

            const labelDiv = document.createElement('div');
            labelDiv.className = 'rule-label';
            labelDiv.textContent = rule.rule;

            const descDiv = document.createElement('div');
            descDiv.className = 'rule-description';
            descDiv.textContent = rule.description;

            ruleDiv.appendChild(labelDiv);
            ruleDiv.appendChild(descDiv);
            followedRulesContainer.appendChild(ruleDiv);
        });
    } else {
        followedRulesContainer.innerHTML = '<div class="no-rules">No rules followed yet</div>';
    }

    // Contradicted rules
    const contradictedRulesContainer = document.getElementById('contradictedRules');
    contradictedRulesContainer.innerHTML = '';

    if (nameAnalysis.contradicted_rules && nameAnalysis.contradicted_rules.length > 0) {
        nameAnalysis.contradicted_rules.forEach(rule => {
            const ruleDiv = document.createElement('div');
            ruleDiv.className = `rule-item ${rule.status}`;

            const labelDiv = document.createElement('div');
            labelDiv.className = 'rule-label';
            labelDiv.textContent = rule.rule;

            const descDiv = document.createElement('div');
            descDiv.className = 'rule-description';
            descDiv.textContent = rule.description;

            ruleDiv.appendChild(labelDiv);
            ruleDiv.appendChild(descDiv);
            contradictedRulesContainer.appendChild(ruleDiv);
        });
    } else {
        contradictedRulesContainer.innerHTML = '<div class="no-rules">✓ All rules are followed! Great name choice!</div>';
    }
}

/**
 * Export results to PDF
 * Uses jsPDF and jsPDF-AutoTable libraries
 */
async function exportToPDF() {
    if (!currentNumerologyData) {
        alert('No data available to export. Please calculate first.');
        return;
    }

    try {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        const data = currentNumerologyData;
        let yPos = 20;

        // Title
        doc.setFontSize(20);
        doc.setTextColor(102, 126, 234);
        doc.text('Numerology Report', 105, yPos, { align: 'center' });
        yPos += 15;

        // Personal Information
        doc.setFontSize(12);
        doc.setTextColor(0, 0, 0);
        doc.text(`Name: ${data.name}`, 20, yPos);
        yPos += 8;
        doc.text(`Date of Birth: ${new Date(data.date_of_birth).toLocaleDateString('en-US', {
            year: 'numeric', month: 'long', day: 'numeric'
        })}`, 20, yPos);
        yPos += 8;
        doc.text(`Gender: ${data.gender.charAt(0).toUpperCase() + data.gender.slice(1)}`, 20, yPos);
        yPos += 15;

        // Main Numbers
        doc.setFontSize(14);
        doc.setTextColor(102, 126, 234);
        doc.text('Your Numbers', 20, yPos);
        yPos += 10;

        doc.setFontSize(11);
        doc.setTextColor(0, 0, 0);
        doc.text(`Driver Number: ${data.driver}`, 20, yPos);
        yPos += 7;
        doc.text(`Conductor Number: ${data.conductor}`, 20, yPos);
        yPos += 7;
        doc.text(`Kua Number: ${data.kua}`, 20, yPos);
        yPos += 12;

        // Present and Missing Numbers
        doc.setFontSize(12);
        doc.setTextColor(26, 89, 40);
        doc.text('Present Numbers:', 20, yPos);
        doc.setTextColor(0, 0, 0);
        doc.text(data.present_numbers.join(', '), 70, yPos);
        yPos += 8;

        if (data.missing_numbers.length > 0) {
            doc.setTextColor(211, 47, 47);
            doc.text('Missing Numbers:', 20, yPos);
            doc.setTextColor(0, 0, 0);
            doc.text(data.missing_numbers.join(', '), 70, yPos);
            yPos += 12;
        }

        // Lucky, Bad, Neutral Numbers
        doc.setFontSize(14);
        doc.setTextColor(102, 126, 234);
        doc.text('Number Summary', 20, yPos);
        yPos += 10;

        doc.setFontSize(11);
        doc.setTextColor(75, 175, 80);
        doc.text('Lucky Numbers:', 20, yPos);
        doc.setTextColor(0, 0, 0);
        doc.text(data.lucky_numbers.join(', ') || 'None', 70, yPos);
        yPos += 7;

        doc.setTextColor(244, 67, 54);
        doc.text('Bad Numbers:', 20, yPos);
        doc.setTextColor(0, 0, 0);
        doc.text(data.bad_numbers.join(', ') || 'None', 70, yPos);
        yPos += 7;

        doc.setTextColor(255, 152, 0);
        doc.text('Neutral Numbers:', 20, yPos);
        doc.setTextColor(0, 0, 0);
        doc.text(data.neutral_numbers.join(', ') || 'None', 70, yPos);
        yPos += 15;

        // Check if we need a new page
        if (yPos > 250) {
            doc.addPage();
            yPos = 20;
        }

        // Remedies Part 1
        if (data.remedies_part1 && data.remedies_part1.length > 0) {
            doc.setFontSize(14);
            doc.setTextColor(102, 126, 234);
            doc.text('Remedies - Part 1', 20, yPos);
            yPos += 10;

            doc.setFontSize(10);
            doc.setTextColor(0, 0, 0);

            data.remedies_part1.forEach(remedy => {
                if (yPos > 270) {
                    doc.addPage();
                    yPos = 20;
                }

                doc.setFont(undefined, 'bold');
                doc.text(`• ${remedy.condition}`, 20, yPos);
                yPos += 6;
                doc.setFont(undefined, 'normal');
                const remedyLines = doc.splitTextToSize(remedy.remedy, 170);
                doc.text(remedyLines, 25, yPos);
                yPos += (remedyLines.length * 5) + 5;
            });
            yPos += 5;
        }

        // Luck Factors
        if (data.luck_factors && data.luck_factors.length > 0) {
            if (yPos > 200) {
                doc.addPage();
                yPos = 20;
            }

            doc.setFontSize(14);
            doc.setTextColor(102, 126, 234);
            doc.text('Luck Factor - Next 6 Years', 20, yPos);
            yPos += 10;

            // Create table data
            const tableData = data.luck_factors.map(item => [
                item.year,
                item.date,
                item.combination,
                item.luck_factor
            ]);

            doc.autoTable({
                startY: yPos,
                head: [['Year', 'Date', 'PY, D', 'Luck Factor']],
                body: tableData,
                theme: 'striped',
                headStyles: { fillColor: [102, 126, 234] },
                margin: { left: 20, right: 20 }
            });

            yPos = doc.lastAutoTable.finalY + 15;
        }

        // Name Numerology Analysis
        if (data.name_analysis) {
            if (yPos > 220) {
                doc.addPage();
                yPos = 20;
            }

            doc.setFontSize(14);
            doc.setTextColor(102, 126, 234);
            doc.text('Name Numerology Analysis', 20, yPos);
            yPos += 10;

            doc.setFontSize(11);
            doc.setTextColor(0, 0, 0);
            doc.text(`First Name: ${data.name_analysis.first_name} = ${data.name_analysis.first_name_value}`, 20, yPos);
            yPos += 7;
            doc.text(`Full Name: ${data.name_analysis.full_name} = ${data.name_analysis.full_name_value}`, 20, yPos);
            yPos += 12;

            // Followed rules
            if (data.name_analysis.followed_rules && data.name_analysis.followed_rules.length > 0) {
                doc.setTextColor(75, 175, 80);
                doc.text('✓ Rules Followed:', 20, yPos);
                yPos += 7;

                doc.setFontSize(10);
                doc.setTextColor(0, 0, 0);
                data.name_analysis.followed_rules.forEach(rule => {
                    if (yPos > 270) {
                        doc.addPage();
                        yPos = 20;
                    }
                    const lines = doc.splitTextToSize(`• ${rule.description}`, 170);
                    doc.text(lines, 25, yPos);
                    yPos += (lines.length * 5) + 3;
                });
                yPos += 5;
            }

            // Contradicted rules
            if (data.name_analysis.contradicted_rules && data.name_analysis.contradicted_rules.length > 0) {
                if (yPos > 250) {
                    doc.addPage();
                    yPos = 20;
                }

                doc.setFontSize(11);
                doc.setTextColor(244, 67, 54);
                doc.text('✗ Rules Contradicted:', 20, yPos);
                yPos += 7;

                doc.setFontSize(10);
                doc.setTextColor(0, 0, 0);
                data.name_analysis.contradicted_rules.forEach(rule => {
                    if (yPos > 270) {
                        doc.addPage();
                        yPos = 20;
                    }
                    const lines = doc.splitTextToSize(`• ${rule.description}`, 170);
                    doc.text(lines, 25, yPos);
                    yPos += (lines.length * 5) + 3;
                });
            }
        }

        // Save the PDF
        const fileName = `Numerology_${data.name.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`;
        doc.save(fileName);

    } catch (error) {
        console.error('PDF Export Error:', error);
        alert('Failed to export PDF. Please make sure you have an internet connection.');
    }
}
