// Global state
let currentAnalysisId = null;
let analysisData = null;

// Example projects
const examples = {
    rag: `We need an AI-powered chatbot using FastAPI and React. The bot should answer questions using RAG (Retrieval Augmented Generation). Users should be able to upload documents and chat with them. Deploy on AWS with authentication.`,
    
    ecommerce: `Build a multi-vendor e-commerce marketplace with product listings, shopping cart, payment processing with Stripe, order management, vendor dashboards, and admin panel. Use React for frontend and Node.js for backend.`,
    
    realtime: `Create a real-time chat application with video calling capabilities. Features: user authentication, one-on-one messaging, group chats, video/audio calls, message history, file sharing. Use WebSockets for real-time communication.`
};

// DOM Elements
const projectInput = document.getElementById('projectInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const inputSection = document.getElementById('inputSection');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
});

function setupEventListeners() {
    // Analyze button
    analyzeBtn.addEventListener('click', analyzeProject);
    
    // Example buttons
    document.querySelectorAll('.btn-example').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const example = e.target.dataset.example;
            projectInput.value = examples[example];
        });
    });
    
    // Tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            switchTab(e.target.dataset.tab);
        });
    });
    
    // Action buttons
    document.getElementById('generateLearningBtn')?.addEventListener('click', generateLearningPath);
    document.getElementById('generatePortfolioBtn')?.addEventListener('click', generatePortfolio);
    document.getElementById('exportBtn')?.addEventListener('click', exportAnalysis);
    document.getElementById('newAnalysisBtn')?.addEventListener('click', newAnalysis);
    document.getElementById('retryBtn')?.addEventListener('click', () => {
        hideError();
        showSection('input');
    });
}

// Main analysis function
async function analyzeProject() {
    const description = projectInput.value.trim();
    
    if (!description) {
        alert('Please enter a project description');
        return;
    }
    
    showSection('loading');
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ description })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }
        
        currentAnalysisId = data.analysis_id;
        analysisData = data;
        
        displayResults(data);
        showSection('results');
        
    } catch (error) {
        showError(error.message);
    }
}

// Display results
function displayResults(data) {
    displaySummary(data);
    displayTechStack(data.tech_detection);
    displayComplexity(data.complexity);
    displayThirdParty(data.third_party);
}

function displaySummary(data) {
    const complexity = data.complexity || {};
    const techDetection = data.tech_detection || {};
    const thirdParty = data.third_party || {};
    
    const explicitTech = techDetection.explicit_technologies || {};
    const techCount = Object.values(explicitTech).reduce((sum, arr) => sum + arr.length, 0);
    
    const html = `
        <div class="summary-grid">
            <div class="summary-item">
                <strong>Skill Level</strong>
                <span>${complexity.skill_level || 'Unknown'}</span>
            </div>
            <div class="summary-item">
                <strong>Complexity Score</strong>
                <span>${complexity.complexity_score || 0}/15</span>
            </div>
            <div class="summary-item">
                <strong>Learning Time</strong>
                <span>${complexity.learning_time || 'Unknown'}</span>
            </div>
            <div class="summary-item">
                <strong>Technologies</strong>
                <span>${techCount}</span>
            </div>
            <div class="summary-item">
                <strong>API Keys Needed</strong>
                <span>${thirdParty.total_api_keys_needed || 0}</span>
            </div>
            <div class="summary-item">
                <strong>Monthly Cost</strong>
                <span>${thirdParty.estimated_monthly_cost || 'Unknown'}</span>
            </div>
        </div>
    `;
    
    document.getElementById('summaryContent').innerHTML = html;
}

function displayTechStack(techDetection) {
    if (!techDetection) {
        document.getElementById('techStackContent').innerHTML = '<p>No tech stack data available</p>';
        return;
    }
    
    let html = '<h4>✅ Explicitly Mentioned Technologies</h4>';
    const explicit = techDetection.explicit_technologies || {};
    
    for (const [category, techs] of Object.entries(explicit)) {
        if (techs && techs.length > 0) {
            html += `
                <div class="tech-category">
                    <h4>${category.toUpperCase()}</h4>
                    <div class="tech-list">
                        ${techs.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
                    </div>
                </div>
            `;
        }
    }
    
    html += '<h4 style="margin-top: 30px;">💡 Implicit Requirements</h4>';
    const implicit = techDetection.implicit_requirements || {};
    
    for (const [category, reqs] of Object.entries(implicit)) {
        if (reqs && reqs.length > 0) {
            html += `
                <div class="tech-category">
                    <h4>${category.toUpperCase()}</h4>
                    <ul>
                        ${reqs.map(req => `<li>${req}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
    }
    
    const missing = techDetection.missing_specifications || [];
    if (missing.length > 0) {
        html += `
            <h4 style="margin-top: 30px;">⚠️ Missing/Unclear Specifications</h4>
            <ul>
                ${missing.map(spec => `<li>${spec}</li>`).join('')}
            </ul>
        `;
    }
    
    document.getElementById('techStackContent').innerHTML = html;
}

function displayComplexity(complexity) {
    if (!complexity) {
        document.getElementById('complexityContent').innerHTML = '<p>No complexity data available</p>';
        return;
    }
    
    const skillClass = `skill-${(complexity.skill_level || 'intermediate').toLowerCase()}`;
    
    let html = `
        <div class="info-grid">
            <div class="info-item">
                <strong>Skill Level</strong>
                <span class="skill-badge ${skillClass}">${complexity.skill_level || 'Unknown'}</span>
            </div>
            <div class="info-item">
                <strong>Complexity Score</strong>
                ${complexity.complexity_score || 0}/15
            </div>
            <div class="info-item">
                <strong>Learning Time</strong>
                ${complexity.learning_time || 'Unknown'}
            </div>
            <div class="info-item">
                <strong>Learning Curve</strong>
                ${(complexity.learning_curve || 'moderate').toUpperCase()}
            </div>
        </div>
    `;
    
    const prereqs = complexity.prerequisite_knowledge || [];
    if (prereqs.length > 0) {
        html += `
            <h4 style="margin-top: 20px;">📋 Prerequisites</h4>
            <ul>
                ${prereqs.map(prereq => `<li>${prereq}</li>`).join('')}
            </ul>
        `;
    }
    
    const coreSkills = complexity.core_skills_required || [];
    if (coreSkills.length > 0) {
        html += `<h4 style="margin-top: 20px;">🎓 Core Skills Required</h4>`;
        coreSkills.forEach(skill => {
            const diffClass = `skill-${(skill.difficulty || 'intermediate').toLowerCase()}`;
            html += `
                <div class="service-item">
                    <h5>${skill.skill} <span class="skill-badge ${diffClass}">${skill.difficulty}</span></h5>
                    <p><strong>Time:</strong> ${skill.learning_time}</p>
                    <p><strong>Why:</strong> ${skill.why_needed}</p>
                </div>
            `;
        });
    }
    
    const challenges = complexity.challenging_concepts || [];
    if (challenges.length > 0) {
        html += `
            <h4 style="margin-top: 20px;">⚠️ Challenging Concepts</h4>
            <ul>
                ${challenges.map(challenge => `<li>${challenge}</li>`).join('')}
            </ul>
        `;
    }
    
    if (complexity.reasoning) {
        html += `
            <h4 style="margin-top: 20px;">💡 Analysis</h4>
            <p>${complexity.reasoning}</p>
        `;
    }
    
    document.getElementById('complexityContent').innerHTML = html;
}

function displayThirdParty(thirdParty) {
    if (!thirdParty) {
        document.getElementById('thirdPartyContent').innerHTML = '<p>No 3rd party data available</p>';
        return;
    }
    
    let html = `
        <div class="info-grid">
            <div class="info-item">
                <strong>API Keys Needed</strong>
                ${thirdParty.total_api_keys_needed || 0}
            </div>
            <div class="info-item">
                <strong>Monthly Cost</strong>
                ${thirdParty.estimated_monthly_cost || 'Unknown'}
            </div>
            <div class="info-item">
                <strong>Free Tier Viable</strong>
                ${thirdParty.free_tier_viable ? '✅ Yes' : '❌ No'}
            </div>
        </div>
    `;
    
    const categories = [
        ['authentication_services', '🔐 Authentication'],
        ['payment_services', '💳 Payment'],
        ['cloud_storage', '☁️ Storage'],
        ['email_services', '📧 Email'],
        ['ai_ml_services', '🤖 AI/ML'],
        ['other_apis', '🔧 Other APIs']
    ];
    
    categories.forEach(([key, title]) => {
        const services = thirdParty[key] || [];
        if (services.length > 0) {
            html += `<h4 style="margin-top: 20px;">${title}</h4>`;
            services.forEach(service => {
                const pricingEmoji = service.pricing === 'free' ? '🆓' : service.pricing === 'freemium' ? '💵' : '💰';
                html += `
                    <div class="service-item">
                        <h5>${service.service} ${pricingEmoji}</h5>
                        <div class="service-details">
                            <div><strong>Purpose:</strong> ${service.purpose}</div>
                            <div><strong>API Key:</strong> ${service.api_key_required ? 'Required' : 'Not required'}</div>
                            <div><strong>Setup:</strong> ${(service.setup_complexity || 'unknown').toUpperCase()}</div>
                        </div>
                        ${service.free_tier_limits ? `<p><strong>Free Tier:</strong> ${service.free_tier_limits}</p>` : ''}
                        ${service.alternatives && service.alternatives.length > 0 ? `<p><strong>Alternatives:</strong> ${service.alternatives.join(', ')}</p>` : ''}
                    </div>
                `;
            });
        }
    });
    
    const setupGuide = thirdParty.setup_guide || [];
    if (setupGuide.length > 0) {
        html += `
            <h4 style="margin-top: 20px;">📋 Setup Guide</h4>
            <ol>
                ${setupGuide.map(step => `<li>${step}</li>`).join('')}
            </ol>
        `;
    }
    
    document.getElementById('thirdPartyContent').innerHTML = html;
}

// Generate learning path
async function generateLearningPath() {
    const btn = document.getElementById('generateLearningBtn');
    const content = document.getElementById('learningContent');
    
    btn.disabled = true;
    btn.textContent = '⏳ Generating...';
    content.innerHTML = '<p>Generating learning path...</p>';
    
    try {
        const response = await fetch(`/api/learning-path/${currentAnalysisId}`);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to generate learning path');
        }
        
        displayLearningPath(data.learning_path);
        btn.style.display = 'none';
        
    } catch (error) {
        content.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        btn.disabled = false;
        btn.textContent = 'Generate Learning Path';
    }
}

function displayLearningPath(learningPath) {
    if (!learningPath) return;
    
    let html = `
        <div class="info-grid">
            <div class="info-item">
                <strong>Total Learning Time</strong>
                ${learningPath.total_learning_time || 'Unknown'}
            </div>
        </div>
    `;
    
    if (learningPath.recommended_sequence) {
        html += `<p><strong>🎯 Strategy:</strong> ${learningPath.recommended_sequence}</p>`;
    }
    
    const learningOrder = learningPath.learning_order || [];
    if (learningOrder.length > 0) {
        html += '<h4 style="margin-top: 20px;">📖 Learning Roadmap</h4>';
        learningOrder.forEach((tech, index) => {
            const priorityEmoji = tech.priority === 'high' ? '🔴' : tech.priority === 'medium' ? '🟡' : '🟢';
            const diffClass = `skill-${(tech.difficulty || 'intermediate').toLowerCase()}`;
            
            html += `
                <div class="learning-step">
                    <h4>${index + 1}. ${tech.technology} ${priorityEmoji}</h4>
                    <div class="step-details">
                        <span class="skill-badge ${diffClass}">${tech.difficulty}</span>
                        <strong>Time:</strong> ${tech.learning_time}
                    </div>
                    ${tech.prerequisites && tech.prerequisites.length > 0 ? `
                        <p><strong>Prerequisites:</strong> ${tech.prerequisites.join(', ')}</p>
                    ` : ''}
                    ${tech.key_concepts && tech.key_concepts.length > 0 ? `
                        <p><strong>🎓 Key Concepts:</strong></p>
                        <ul>
                            ${tech.key_concepts.slice(0, 5).map(concept => `<li>${concept}</li>`).join('')}
                        </ul>
                    ` : ''}
                </div>
            `;
        });
    }
    
    document.getElementById('learningContent').innerHTML = html;
}

// Generate portfolio adaptation
async function generatePortfolio() {
    const btn = document.getElementById('generatePortfolioBtn');
    const content = document.getElementById('portfolioContent');
    
    btn.disabled = true;
    btn.textContent = '⏳ Generating...';
    content.innerHTML = '<p>Generating portfolio ideas...</p>';
    
    try {
        const response = await fetch(`/api/portfolio/${currentAnalysisId}`);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to generate portfolio adaptation');
        }
        
        displayPortfolio(data.portfolio_adaptation);
        btn.style.display = 'none';
        
    } catch (error) {
        content.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        btn.disabled = false;
        btn.textContent = 'Generate Portfolio Ideas';
    }
}

function displayPortfolio(portfolio) {
    if (!portfolio || !portfolio.portfolio_version) return;
    
    const pv = portfolio.portfolio_version;
    
    let html = `
        <h4>📌 ${pv.title || 'Portfolio Project'}</h4>
        ${pv.tagline ? `<p><em>${pv.tagline}</em></p>` : ''}
        ${pv.estimated_build_time ? `<p><strong>⏱️ Build Time:</strong> ${pv.estimated_build_time}</p>` : ''}
    `;
    
    if (pv.mvp_features && pv.mvp_features.length > 0) {
        html += `
            <h4 style="margin-top: 20px;">✅ MVP Features</h4>
            <ul>
                ${pv.mvp_features.map(feature => `<li>${feature}</li>`).join('')}
            </ul>
        `;
    }
    
    if (pv.unique_twist) {
        html += `
            <h4 style="margin-top: 20px;">🎯 Unique Twist</h4>
            <p>${pv.unique_twist}</p>
        `;
    }
    
    const deployment = portfolio.deployment_suggestions || [];
    if (deployment.length > 0) {
        html += '<h4 style="margin-top: 20px;">🚀 Deployment Options</h4>';
        deployment.forEach(option => {
            const costEmoji = option.cost === 'free' ? '🆓' : '💰';
            html += `
                <div class="service-item">
                    <h5>${option.platform} ${costEmoji}</h5>
                    <p><strong>Difficulty:</strong> ${(option.difficulty || 'unknown').toUpperCase()}</p>
                    <p>${option.why}</p>
                </div>
            `;
        });
    }
    
    document.getElementById('portfolioContent').innerHTML = html;
}

// Export analysis
async function exportAnalysis() {
    try {
        const response = await fetch(`/api/export/${currentAnalysisId}`);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Export failed');
        }
        
        const dataStr = JSON.stringify(result.data, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `learning_analysis_${currentAnalysisId}.json`;
        link.click();
        URL.revokeObjectURL(url);
        
    } catch (error) {
        alert('Export failed: ' + error.message);
    }
}

// UI helpers
function switchTab(tabName) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.toggle('active', pane.id === tabName);
    });
}

function showSection(section) {
    inputSection.style.display = section === 'input' ? 'block' : 'none';
    loadingSection.style.display = section === 'loading' ? 'block' : 'none';
    resultsSection.style.display = section === 'results' ? 'block' : 'none';
    errorSection.style.display = 'none';
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    inputSection.style.display = 'none';
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'block';
}

function hideError() {
    errorSection.style.display = 'none';
}

function newAnalysis() {
    projectInput.value = '';
    currentAnalysisId = null;
    analysisData = null;
    showSection('input');
}
