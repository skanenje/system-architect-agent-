"""
Upwork Task Analyzer Agent

Analyzes Upwork job postings to determine complexity, tech requirements, and recommendations.
"""

import os
import google.generativeai as genai
from typing import Dict, List, Any, Optional

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

from .memory import ProjectMemory
from ..engines.requirements_extractor import RequirementsExtractor
from ..engines.complexity_analyzer import ComplexityAnalyzer
from ..engines.tech_detector import TechDetector
from ..engines.tech_stack_recommender import TechStackRecommender
from ..engines.learning_path_generator import LearningPathGenerator
from ..engines.third_party_detector import ThirdPartyDetector
from ..engines.portfolio_adapter import PortfolioAdapter


class TechStackLearningAnalyzer:
    """
    Tech Stack Learning Analyzer
    
    Analyzes projects (Upwork jobs, portfolio ideas, etc.) to provide:
    - Tech stack identification
    - Learning path generation
    - Skill complexity analysis
    - 3rd party requirements detection
    - Portfolio adaptation suggestions
    """
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.memory = ProjectMemory(project_id)
        
        # Initialize all engines
        self.req_extractor = RequirementsExtractor()
        self.complexity_analyzer = ComplexityAnalyzer()
        self.tech_detector = TechDetector()
        self.tech_recommender = TechStackRecommender()
        self.learning_path_generator = LearningPathGenerator()
        self.third_party_detector = ThirdPartyDetector()
        self.portfolio_adapter = PortfolioAdapter()
        
        self.analysis_complete = False
    
    def analyze(self, project_description: str, generate_learning_path: bool = True) -> str:
        """
        Analyze project for learning purposes.
        
        Args:
            project_description: Project description (Upwork job, portfolio idea, etc.)
            generate_learning_path: Whether to generate detailed learning path
            
        Returns:
            Formatted analysis output
        """
        output_sections = []
        
        # Store project description
        self.memory.set_job_description(project_description)
        
        # ===== STEP 1: Extract Requirements =====
        print("📋 Extracting requirements...")
        requirements = self.req_extractor.extract(project_description)
        
        for category, reqs in requirements.items():
            if reqs:
                self.memory.add_requirements_batch(category, reqs)
        
        output_sections.append(self.req_extractor.format_requirements(requirements))
        
        # ===== STEP 2: Detect Tech Stack =====
        print("🛠️  Detecting tech stack...")
        tech_detection = self.tech_detector.detect(project_description)
        self.memory.set_tech_detection(tech_detection)
        output_sections.append(self.tech_detector.format_detection(tech_detection))
        
        # ===== STEP 3: Analyze Skill Complexity =====
        print("📊 Analyzing skill complexity...")
        complexity = self.complexity_analyzer.analyze(project_description)
        self.memory.set_complexity_analysis(complexity)
        output_sections.append(self.complexity_analyzer.format_analysis(complexity))
        
        # ===== STEP 4: Detect 3rd Party Requirements =====
        print("🔌 Detecting 3rd party requirements...")
        functional_reqs = [r['text'] if isinstance(r, dict) else r for r in requirements.get('functional', [])]
        third_party = self.third_party_detector.detect(project_description, functional_reqs)
        self.memory.data['third_party_requirements'] = third_party
        output_sections.append(self.third_party_detector.format_third_party(third_party))
        
        # ===== STEP 5: Generate Learning Path (Optional) =====
        if generate_learning_path:
            print("📚 Generating learning path...")
            learning_path = self.learning_path_generator.generate(project_description, tech_detection)
            self.memory.data['learning_path'] = learning_path
            output_sections.append(self.learning_path_generator.format_learning_path(learning_path))
        
        # ===== Final Summary =====
        self.analysis_complete = True
        
        summary = f"\n{'=' * 70}\n🎯 TECH STACK LEARNING ANALYSIS\n{'=' * 70}\n"
        summary += self.memory.get_summary()
        
        output_sections.insert(0, summary)
        
        return "\n\n".join(output_sections)
    
    def show_complexity(self) -> str:
        """Display skill complexity analysis."""
        complexity = self.memory.get_complexity_analysis()
        if not complexity:
            return "No complexity analysis available yet."
        return self.complexity_analyzer.format_analysis(complexity)
    
    def show_tech_stack(self) -> str:
        """Display tech detection."""
        detection = self.memory.get_tech_detection()
        if not detection:
            return "No tech stack information available."
        return self.tech_detector.format_detection(detection)
    
    def show_learning_path(self) -> str:
        """Display learning path and roadmap."""
        learning_path = self.memory.data.get('learning_path')
        if not learning_path:
            return "No learning path generated yet."
        return self.learning_path_generator.format_learning_path(learning_path)
    
    def show_third_party(self) -> str:
        """Display 3rd party requirements."""
        third_party = self.memory.data.get('third_party_requirements')
        if not third_party:
            return "No 3rd party requirements detected."
        return self.third_party_detector.format_third_party(third_party)
    
    def show_portfolio_adaptation(self) -> str:
        """Generate and display portfolio adaptation."""
        complexity = self.memory.get_complexity_analysis()
        skill_level = complexity.get('skill_level', 'INTERMEDIATE') if complexity else 'INTERMEDIATE'
        
        print("🎨 Generating portfolio adaptation...")
        adaptation = self.portfolio_adapter.adapt(
            self.memory.get_job_description() or "",
            skill_level
        )
        self.memory.data['portfolio_adaptation'] = adaptation
        return self.portfolio_adapter.format_portfolio_adaptation(adaptation)
    
    def export_to_json(self) -> str:
        """Export complete analysis as JSON."""
        return self.memory.to_json(pretty=True)


# Backward compatibility aliases
UpworkAnalyzer = TechStackLearningAnalyzer
ArchitectureAgent = TechStackLearningAnalyzer
