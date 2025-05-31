document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const inputText = document.getElementById('input-text');
    const processBtn = document.getElementById('process-btn');
    const errorAlert = document.getElementById('error-alert');
    const errorMessage = document.querySelector('.alert-message');
    const resultCard = document.getElementById('result-card');
    const loadingOverlay = document.getElementById('loading-overlay');
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    const emailSample = document.getElementById('email-sample');
    const jsonSample = document.getElementById('json-sample');
    const textSample = document.getElementById('text-sample');
    const clearMemoryBtn = document.getElementById('clear-memory');
    const memoryEntries = document.getElementById('memory-entries');
    const emptyMemory = document.getElementById('empty-memory');

    // Result elements
    const resultFormat = document.getElementById('result-format');
    const resultIntent = document.getElementById('result-intent');
    const resultConfidence = document.getElementById('result-confidence');
    const resultReasoning = document.getElementById('result-reasoning');
    const resultData = document.getElementById('result-data');
    const anomaliesSection = document.getElementById('anomalies-section');
    const anomaliesList = document.getElementById('anomalies-list');
    const memoryId = document.getElementById('memory-id');
    const timestamp = document.getElementById('timestamp');
    const agentBadge = document.getElementById('agent-badge');
    const reasoningSection = document.getElementById('reasoning-section');

    // Current input type
    let currentInputType = 'email';

    // Sample data
    const samples = {
        email: `From: john.doe@acmecorp.com
Subject: Urgent RFQ - Manufacturing Equipment

Hi there,

We need a quote for 50 units of industrial pumps for our new facility. 
This is urgent as we need to finalize our vendor selection by Friday.

Specifications:
- Flow rate: 100 GPM
- Pressure: 150 PSI
- Material: Stainless steel

Please send your best pricing and delivery timeline.

Best regards,
John Doe
Procurement Manager
ACME Corp`,
        json: `{
  "webhook_type": "invoice_received",
  "invoice_id": "INV-2024-001",
  "vendor": "TechSupply Inc",
  "amount": 15750.00,
  "currency": "USD",
  "due_date": "2024-02-15",
  "line_items": [
    {
      "description": "Server Hardware",
      "quantity": 2,
      "unit_price": 5000.00,
      "total": 10000.00
    },
    {
      "description": "Network Equipment",
      "quantity": 1,
      "unit_price": 5750.00,
      "total": 5750.00
    }
  ],
  "status": "pending_approval"
}`,
        text: `REGULATION NOTICE: New environmental compliance requirements for manufacturing facilities effective March 1, 2024. All facilities must implement waste reduction protocols and submit quarterly reports. Companies must designate a compliance officer and submit initial assessment by April 15, 2024.`
    };

    // Tab switching
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabType = tab.dataset.tab;
            
            // Update active tab
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Show corresponding content
            tabContents.forEach(content => content.classList.add('hidden'));
            document.getElementById(`${tabType}-content`).classList.remove('hidden');
            
            // Update current input type
            currentInputType = tabType;
        });
    });

    // Load sample data
    emailSample.addEventListener('click', () => inputText.value = samples.email);
    jsonSample.addEventListener('click', () => inputText.value = samples.json);
    textSample.addEventListener('click', () => inputText.value = samples.text);

    // Process button click
    processBtn.addEventListener('click', async () => {
        const input = inputText.value.trim();
        if (!input) return;

        // Show loading overlay
        loadingOverlay.classList.remove('hidden');
        errorAlert.classList.add('hidden');
        resultCard.classList.add('hidden');

        try {
            // Call classifier API
            const response = await fetch('/api/agents/classifier', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ input, inputType: currentInputType })
            });

            const data = await response.json();

            if (response.ok) {
                displayResult(data);
                fetchMemory();
            } else {
                throw new Error(data.error || data.details || 'Processing failed');
            }
        } catch (error) {
            console.error('Error:', error);
            errorMessage.textContent = error.message || 'An error occurred during processing';
            errorAlert.classList.remove('hidden');
        } finally {
            loadingOverlay.classList.add('hidden');
        }
    });

    // Clear memory button
    clearMemoryBtn.addEventListener('click', async () => {
        try {
            await fetch('/api/memory', { method: 'DELETE' });
            fetchMemory();
        } catch (error) {
            console.error('Failed to clear memory:', error);
        }
    });

    // Display result
    function displayResult(data) {
        // Show result card
        resultCard.classList.remove('hidden');

        // Set classification data
        resultFormat.textContent = data.classification.format || 'Unknown';
        resultIntent.textContent = data.classification.intent || 'Unknown';
        resultConfidence.textContent = `${Math.round((data.classification.confidence || 0) * 100)}%`;
        
        // Set reasoning if available
        if (data.classification.reasoning) {
            resultReasoning.textContent = data.classification.reasoning;
            reasoningSection.classList.remove('hidden');
        } else {
            reasoningSection.classList.add('hidden');
        }
        
        // Set extracted data
        resultData.textContent = JSON.stringify(data.extracted_data, null, 2);
        
        // Set anomalies if any
        if (data.anomalies && data.anomalies.length > 0) {
            anomaliesList.innerHTML = '';
            data.anomalies.forEach(anomaly => {
                const li = document.createElement('li');
                li.textContent = anomaly;
                anomaliesList.appendChild(li);
            });
            anomaliesSection.classList.remove('hidden');
        } else {
            anomaliesSection.classList.add('hidden');
        }
        
        // Set metadata
        memoryId.textContent = data.memory_id || '-';
        timestamp.textContent = data.timestamp ? new Date(data.timestamp).toLocaleString() : '-';
        
        // Set agent badge
        agentBadge.textContent = data.processing_agent || 'classifier_agent';
    }

    // Fetch memory entries
    async function fetchMemory() {
        try {
            const response = await fetch('/api/memory');
            const data = await response.json();
            
            if (response.ok && data.entries) {
                if (data.entries.length === 0) {
                    emptyMemory.classList.remove('hidden');
                    memoryEntries.classList.add('hidden');
                } else {
                    emptyMemory.classList.add('hidden');
                    memoryEntries.classList.remove('hidden');
                    
                    // Display memory entries
                    memoryEntries.innerHTML = '';
                    
                    // Get last 10 entries and reverse them (newest first)
                    const entries = data.entries.slice(-10).reverse();
                    
                    entries.forEach(entry => {
                        const memoryItem = document.createElement('div');
                        memoryItem.className = 'memory-item';
                        
                        const header = document.createElement('div');
                        header.className = 'memory-header';
                        
                        const badges = document.createElement('div');
                        badges.className = 'memory-badges';
                        
                        const formatBadge = document.createElement('span');
                        formatBadge.className = 'badge outline';
                        formatBadge.textContent = entry.format || 'unknown';
                        
                        const intentBadge = document.createElement('span');
                        intentBadge.className = 'badge secondary';
                        intentBadge.textContent = entry.intent || 'unknown';
                        
                        badges.appendChild(formatBadge);
                        badges.appendChild(intentBadge);
                        
                        const time = document.createElement('span');
                        time.className = 'memory-time';
                        time.textContent = entry.timestamp ? new Date(entry.timestamp).toLocaleTimeString() : 'unknown';
                        
                        header.appendChild(badges);
                        header.appendChild(time);
                        
                        const content = document.createElement('p');
                        content.className = 'memory-content';
                        content.textContent = entry.source ? `${entry.source.substring(0, 150)}...` : 'No source data';
                        
                        memoryItem.appendChild(header);
                        memoryItem.appendChild(content);
                        
                        memoryEntries.appendChild(memoryItem);
                    });
                }
            }
        } catch (error) {
            console.error('Failed to fetch memory:', error);
        }
    }

    // Auto-resize textarea
    inputText.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // Initial memory fetch
    fetchMemory();
});