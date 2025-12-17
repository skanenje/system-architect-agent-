"""
Flask Web Server for Tech Stack Learning Analyzer
"""

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import uuid
import traceback

load_dotenv()

from src.system_architect.core.agent import TechStackLearningAnalyzer

app = Flask(__name__)

# Store analyzers in memory (in production, use a database)
analyzers = {}


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze a project description"""
    try:
        data = request.json
        project_description = data.get('description', '').strip()
        
        if not project_description:
            return jsonify({'error': 'Please provide a project description'}), 400
        
        # Create analyzer
        analysis_id = str(uuid.uuid4())[:8]
        analyzer = TechStackLearningAnalyzer(analysis_id)
        analyzers[analysis_id] = analyzer
        
        # Run analysis (without full learning path for speed)
        print(f"Analyzing project {analysis_id}...")
        analyzer.analyze(project_description, generate_learning_path=False)
        
        # Get results
        complexity = analyzer.memory.get_complexity_analysis()
        tech_detection = analyzer.memory.get_tech_detection()
        third_party = analyzer.memory.data.get('third_party_requirements')
        
        return jsonify({
            'success': True,
            'analysis_id': analysis_id,
            'complexity': complexity,
            'tech_detection': tech_detection,
            'third_party': third_party,
            'summary': analyzer.memory.get_summary()
        })
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/learning-path/<analysis_id>', methods=['GET'])
def get_learning_path(analysis_id):
    """Generate learning path for an analysis"""
    try:
        analyzer = analyzers.get(analysis_id)
        if not analyzer:
            return jsonify({'error': 'Analysis not found'}), 404
        
        # Check if already generated
        if analyzer.memory.data.get('learning_path'):
            return jsonify({
                'success': True,
                'learning_path': analyzer.memory.data['learning_path']
            })
        
        # Generate learning path
        print(f"Generating learning path for {analysis_id}...")
        project_description = analyzer.memory.get_job_description()
        tech_detection = analyzer.memory.get_tech_detection()
        
        learning_path = analyzer.learning_path_generator.generate(
            project_description,
            tech_detection
        )
        analyzer.memory.data['learning_path'] = learning_path
        
        return jsonify({
            'success': True,
            'learning_path': learning_path
        })
        
    except Exception as e:
        print(f"Error generating learning path: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/portfolio/<analysis_id>', methods=['GET'])
def get_portfolio_adaptation(analysis_id):
    """Generate portfolio adaptation for an analysis"""
    try:
        analyzer = analyzers.get(analysis_id)
        if not analyzer:
            return jsonify({'error': 'Analysis not found'}), 404
        
        # Check if already generated
        if analyzer.memory.data.get('portfolio_adaptation'):
            return jsonify({
                'success': True,
                'portfolio_adaptation': analyzer.memory.data['portfolio_adaptation']
            })
        
        # Generate portfolio adaptation
        print(f"Generating portfolio adaptation for {analysis_id}...")
        project_description = analyzer.memory.get_job_description()
        complexity = analyzer.memory.get_complexity_analysis()
        skill_level = complexity.get('skill_level', 'INTERMEDIATE') if complexity else 'INTERMEDIATE'
        
        portfolio_adaptation = analyzer.portfolio_adapter.adapt(
            project_description,
            skill_level
        )
        analyzer.memory.data['portfolio_adaptation'] = portfolio_adaptation
        
        return jsonify({
            'success': True,
            'portfolio_adaptation': portfolio_adaptation
        })
        
    except Exception as e:
        print(f"Error generating portfolio adaptation: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/<analysis_id>', methods=['GET'])
def export_analysis(analysis_id):
    """Export complete analysis as JSON"""
    try:
        analyzer = analyzers.get(analysis_id)
        if not analyzer:
            return jsonify({'error': 'Analysis not found'}), 404
        
        return jsonify({
            'success': True,
            'data': analyzer.memory.data
        })
        
    except Exception as e:
        print(f"Error exporting analysis: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🚀 Tech Stack Learning Analyzer - Web UI")
    print("=" * 70)
    print("\n📱 Open your browser and go to: http://localhost:5000")
    print("\n💡 Press Ctrl+C to stop the server\n")
    print("=" * 70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
