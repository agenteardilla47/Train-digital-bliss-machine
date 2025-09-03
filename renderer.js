// TECS Desktop Application - Renderer Process

class TECSDesktop {
    constructor() {
        this.currentTab = 'tecs';
        this.operationsLog = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupPythonStatusListener();
        this.updateSystemInfo();
        this.setBuildDate();
        this.setupRangeInputs();
    }

    setupEventListeners() {
        // Tab navigation
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // TECS execution
        document.getElementById('executeTecsBtn').addEventListener('click', () => {
            this.executeTECS();
        });

        // CF execution
        document.getElementById('executeCfBtn').addEventListener('click', () => {
            this.executeCF();
        });

        // Settings
        document.getElementById('settingsBtn').addEventListener('click', () => {
            this.showSettings();
        });

        document.getElementById('closeSettingsBtn').addEventListener('click', () => {
            this.hideSettings();
        });

        document.getElementById('cancelSettingsBtn').addEventListener('click', () => {
            this.hideSettings();
        });

        document.getElementById('saveSettingsBtn').addEventListener('click', () => {
            this.saveSettings();
        });

        // Install dependencies
        document.getElementById('installDepsBtn').addEventListener('click', () => {
            this.installDependencies();
        });
    }

    setupPythonStatusListener() {
        window.electronAPI.onPythonStatus((event, data) => {
            this.updatePythonStatus(data);
        });
    }

    setupRangeInputs() {
        const entropyRange = document.getElementById('tecsCollaboratorEntropy');
        const entropyValue = document.getElementById('tecsEntropyValue');
        
        if (entropyRange && entropyValue) {
            entropyRange.addEventListener('input', (e) => {
                entropyValue.textContent = e.target.value;
            });
        }
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');

        this.currentTab = tabName;
    }

    updatePythonStatus(data) {
        const statusElement = document.getElementById('pythonStatus');
        const statusIndicator = statusElement.querySelector('.status-indicator');
        const statusText = statusElement.querySelector('.status-text');

        statusText.textContent = data.message;

        // Update status indicator
        statusIndicator.className = 'fas fa-circle status-indicator';
        if (data.status === 'ready') {
            statusIndicator.classList.add('ready');
        } else if (data.status === 'error' || data.status === 'not-found') {
            statusIndicator.classList.add('error');
        }

        // Update monitor tab
        this.updatePythonMonitor(data);

        // Show/hide install dependencies button
        const installBtn = document.getElementById('installDepsBtn');
        if (data.status === 'missing-deps' && installBtn) {
            installBtn.style.display = 'inline-flex';
        } else if (installBtn) {
            installBtn.style.display = 'none';
        }
    }

    updatePythonMonitor(data) {
        const statusValue = document.getElementById('pythonStatusValue');
        const depsValue = document.getElementById('pythonDeps');

        if (statusValue) {
            statusValue.textContent = data.status === 'ready' ? 'Ready' : 
                                    data.status === 'missing-deps' ? 'Missing Dependencies' :
                                    data.status === 'not-found' ? 'Not Found' : 'Error';
        }

        if (depsValue) {
            if (data.status === 'ready') {
                depsValue.textContent = 'All Installed';
            } else if (data.status === 'missing-deps' && data.missing) {
                depsValue.textContent = `Missing: ${data.missing.join(', ')}`;
            } else {
                depsValue.textContent = 'Unknown';
            }
        }
    }

    updateSystemInfo() {
        // Platform info
        const platformInfo = document.getElementById('platformInfo');
        if (platformInfo) {
            platformInfo.textContent = window.electronAPI.platform;
        }

        // Node.js version
        const nodeVersion = document.getElementById('nodeVersion');
        if (nodeVersion) {
            nodeVersion.textContent = window.electronAPI.versions.node;
        }

        // Electron version
        const electronVersion = document.getElementById('electronVersion');
        if (electronVersion) {
            electronVersion.textContent = window.electronAPI.versions.electron;
        }
    }

    setBuildDate() {
        const buildDate = document.getElementById('buildDate');
        if (buildDate) {
            buildDate.textContent = new Date().toLocaleDateString();
        }
    }

    async executeTECS() {
        const sourceData = document.getElementById('tecsSourceData').value.trim();
        if (!sourceData) {
            this.showError('Please enter source data for TECS processing.');
            return;
        }

        const collaboratorType = document.getElementById('tecsCollaboratorType').value;
        const collaboratorEntropy = parseFloat(document.getElementById('tecsCollaboratorEntropy').value);
        const securityLevel = parseInt(document.getElementById('tecsSecurityLevel').value);

        const collaboratorProfile = {
            entropy: collaboratorEntropy,
            type: collaboratorType,
            domain: this.getDomainFromType(collaboratorType)
        };

        this.showLoading('Executing TECS Protocol', 'Processing thermodynamic phase transitions...');

        try {
            const result = await window.electronAPI.executeTECS({
                sourceData,
                collaboratorProfile,
                securityLevel
            });

            this.hideLoading();
            this.displayTECSResults(result);
            this.logOperation('TECS Protocol executed successfully');
        } catch (error) {
            this.hideLoading();
            this.showError(`TECS execution failed: ${error.message}`);
            this.logOperation(`TECS Protocol failed: ${error.message}`);
        }
    }

    async executeCF() {
        const sourceData = document.getElementById('cfSourceData').value.trim();
        if (!sourceData) {
            this.showError('Please enter source data for CF processing.');
            return;
        }

        const taskType = document.getElementById('cfTaskType').value;
        const regularization = document.getElementById('cfRegularization').value;
        const securityLevel = parseInt(document.getElementById('cfSecurityLevel').value);

        const functionalRequirements = {
            task_type: taskType,
            regularization: regularization
        };

        this.showLoading('Executing CF Protocol', 'Processing cryptographic forgetting...');

        try {
            const result = await window.electronAPI.executeCF({
                sourceData,
                functionalRequirements,
                securityLevel
            });

            this.hideLoading();
            this.displayCFResults(result);
            this.logOperation('CF Protocol executed successfully');
        } catch (error) {
            this.hideLoading();
            this.showError(`CF execution failed: ${error.message}`);
            this.logOperation(`CF Protocol failed: ${error.message}`);
        }
    }

    getDomainFromType(type) {
        const domainMap = {
            'human_ai_collaboration': 'collaborative_ai',
            'creative_writing': 'creative_writing',
            'scientific_research': 'scientific_research',
            'business_analysis': 'business_analysis',
            'custom': 'general'
        };
        return domainMap[type] || 'general';
    }

    displayTECSResults(result) {
        // Show results section
        document.getElementById('tecsResults').style.display = 'block';

        // Output
        document.getElementById('tecsOutput').textContent = result.output || 'No output generated';

        // Thermodynamic metrics
        document.getElementById('tecsTemp').textContent = result.cognitive_temperature?.toFixed(4) || 'N/A';
        document.getElementById('tecsEntropy').textContent = result.entropy_gradient?.toFixed(6) || 'N/A';
        document.getElementById('tecsPhase').textContent = result.phase_trace || 'N/A';

        // Security information
        document.getElementById('tecsResonance').textContent = this.truncateHash(result.resonance_commitment);
        document.getElementById('tecsRoot').textContent = this.truncateHash(result.thermodynamic_root);
        document.getElementById('tecsProofs').textContent = result.deletion_proofs?.length || 0;

        // Performance metrics
        this.displayPerformanceMetrics('tecsPerformance', result.performance_metrics);
    }

    displayCFResults(result) {
        // Show results section
        document.getElementById('cfResults').style.display = 'block';

        // Output
        document.getElementById('cfOutput').textContent = result.output || 'No output generated';

        // Security information
        document.getElementById('cfProofSize').textContent = `${result.proof_size} bytes`;
        document.getElementById('cfCertificates').textContent = result.certificates_count || 0;
        document.getElementById('cfSecurityParam').textContent = `${result.security_parameters?.security_parameter || 'N/A'} bits`;

        // Performance metrics
        this.displayPerformanceMetrics('cfPerformance', result.performance_metrics);
    }

    displayPerformanceMetrics(elementId, metrics) {
        const element = document.getElementById(elementId);
        if (!element || !metrics) return;

        element.innerHTML = '';

        if (metrics.phase_times) {
            Object.entries(metrics.phase_times).forEach(([phase, time]) => {
                const phaseDiv = document.createElement('div');
                phaseDiv.className = 'metric';
                phaseDiv.innerHTML = `
                    <span class="metric-label">${this.formatPhaseName(phase)}:</span>
                    <span class="metric-value">${time.toFixed(3)}s</span>
                `;
                element.appendChild(phaseDiv);
            });
        }

        if (metrics.total_time) {
            const totalDiv = document.createElement('div');
            totalDiv.className = 'metric';
            totalDiv.innerHTML = `
                <span class="metric-label">Total Time:</span>
                <span class="metric-value">${metrics.total_time.toFixed(3)}s</span>
            `;
            element.appendChild(totalDiv);
        }

        if (metrics.efficiency) {
            const efficiencyDiv = document.createElement('div');
            efficiencyDiv.className = 'metric';
            efficiencyDiv.innerHTML = `
                <span class="metric-label">Efficiency:</span>
                <span class="metric-value">${(metrics.efficiency * 100).toFixed(1)}%</span>
            `;
            element.appendChild(efficiencyDiv);
        }
    }

    formatPhaseName(phase) {
        return phase.split('_').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
    }

    truncateHash(hash, length = 16) {
        if (!hash) return 'N/A';
        return hash.length > length ? hash.substring(0, length) + '...' : hash;
    }

    async installDependencies() {
        const installBtn = document.getElementById('installDepsBtn');
        const originalText = installBtn.innerHTML;
        
        installBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Installing...';
        installBtn.disabled = true;

        try {
            await window.electronAPI.installDependencies();
            this.showSuccess('Dependencies installed successfully!');
            this.logOperation('Python dependencies installed');
        } catch (error) {
            this.showError(`Failed to install dependencies: ${error.message}`);
            this.logOperation(`Dependency installation failed: ${error.message}`);
        } finally {
            installBtn.innerHTML = originalText;
            installBtn.disabled = false;
        }
    }

    showSettings() {
        document.getElementById('settingsModal').style.display = 'flex';
    }

    hideSettings() {
        document.getElementById('settingsModal').style.display = 'none';
    }

    saveSettings() {
        const pythonPath = document.getElementById('pythonPath').value;
        const defaultSecurity = document.getElementById('defaultSecurity').value;
        const enableTee = document.getElementById('enableTee').checked;

        // Save settings (in a real app, this would persist to storage)
        localStorage.setItem('tecs_settings', JSON.stringify({
            pythonPath,
            defaultSecurity,
            enableTee
        }));

        this.showSuccess('Settings saved successfully!');
        this.hideSettings();
    }

    showLoading(title, message) {
        document.getElementById('loadingTitle').textContent = title;
        document.getElementById('loadingMessage').textContent = message;
        document.getElementById('loadingOverlay').style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loadingOverlay').style.display = 'none';
    }

    showError(message) {
        // Simple error display - in a real app, you might want a toast notification
        alert(`Error: ${message}`);
    }

    showSuccess(message) {
        // Simple success display - in a real app, you might want a toast notification
        alert(`Success: ${message}`);
    }

    logOperation(message) {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = { time: timestamp, message };
        
        this.operationsLog.unshift(logEntry);
        if (this.operationsLog.length > 50) {
            this.operationsLog = this.operationsLog.slice(0, 50);
        }

        this.updateOperationsLog();
    }

    updateOperationsLog() {
        const logElement = document.getElementById('operationsLog');
        if (!logElement) return;

        if (this.operationsLog.length === 0) {
            logElement.innerHTML = `
                <div class="log-entry">
                    <span class="log-time">--:--:--</span>
                    <span class="log-message">No operations yet</span>
                </div>
            `;
            return;
        }

        logElement.innerHTML = this.operationsLog.map(entry => `
            <div class="log-entry">
                <span class="log-time">${entry.time}</span>
                <span class="log-message">${entry.message}</span>
            </div>
        `).join('');
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TECSDesktop();
});