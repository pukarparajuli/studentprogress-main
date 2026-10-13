from django.db.models import Avg, Count
from .models import Student, Grade, Attendance
from datetime import datetime, timedelta

class StudentPerformancePredictor:
    @staticmethod
    def calculate_risk_score(student):
        try:
            recent_date = datetime.now().date() - timedelta(days=30)
            recent_grades = Grade.objects.filter(student=student, date__gte=recent_date)
            recent_attendance = Attendance.objects.filter(student=student, date__gte=recent_date)
            
            risk_factors = []
            
            # Grade performance
            if recent_grades.exists():
                avg_percentage = recent_grades.aggregate(avg=Avg('marks'))['avg'] or 0
                if avg_percentage < 40:
                    risk_factors.append(40)
                elif avg_percentage < 60:
                    risk_factors.append(25)
                elif avg_percentage < 75:
                    risk_factors.append(10)
                else:
                    risk_factors.append(0)
            else:
                risk_factors.append(20)
            
            # Attendance rate
            if recent_attendance.exists():
                attendance_rate = recent_attendance.filter(is_present=True).count() / recent_attendance.count() * 100
                if attendance_rate < 70:
                    risk_factors.append(35)
                elif attendance_rate < 85:
                    risk_factors.append(20)
                elif attendance_rate < 95:
                    risk_factors.append(8)
                else:
                    risk_factors.append(0)
            else:
                risk_factors.append(15)
            
            return min(sum(risk_factors), 100)
        except:
            return 50

    @staticmethod
    def get_risk_level(risk_score):
        if risk_score >= 70:
            return "High Risk", "danger"
        elif risk_score >= 40:
            return "Medium Risk", "warning"
        elif risk_score >= 20:
            return "Low Risk", "info"
        else:
            return "On Track", "success"

    @staticmethod
    def get_recommendations(student, risk_score):
        recommendations = []
        
        try:
            recent_date = datetime.now().date() - timedelta(days=30)
            recent_grades = Grade.objects.filter(student=student, date__gte=recent_date)
            recent_attendance = Attendance.objects.filter(student=student, date__gte=recent_date)
            
            if recent_grades.exists():
                avg_grade = recent_grades.aggregate(avg=Avg('marks'))['avg']
                if avg_grade < 60:
                    recommendations.append("Focus on improving academic performance")
                    recommendations.append("Consider additional tutoring")
            
            if recent_attendance.exists():
                attendance_rate = recent_attendance.filter(is_present=True).count() / recent_attendance.count() * 100
                if attendance_rate < 85:
                    recommendations.append("Improve attendance")
                    recommendations.append("Address attendance barriers")
            
            if risk_score >= 70:
                recommendations.append("Immediate intervention required")
            elif risk_score >= 40:
                recommendations.append("Monitor progress closely")
            
            if not recommendations:
                recommendations.append("Keep up the excellent work!")
                recommendations.append("Continue current study habits")
        except:
            recommendations = ["Complete more activities to get insights"]
        
        return recommendations

class GradeAnalyzer:
    @staticmethod
    def analyze_subject_performance(student, subject=None):
        try:
            if subject:
                grades = Grade.objects.filter(student=student, subject=subject).order_by('date')
            else:
                grades = Grade.objects.filter(student=student).order_by('date')
            
            if not grades.exists():
                return {
                    'trend': 'No Data',
                    'average': 0,
                    'improvement_needed': True,
                    'insights': ['No grades recorded yet'],
                    'total_assessments': 0,
                    'class_rank': 'N/A'
                }
            
            total_grades = grades.count()
            average_score = sum(g.marks for g in grades) / total_grades
            
            insights = []
            if average_score >= 85:
                insights.append('Excellent performance!')
            elif average_score >= 70:
                insights.append('Good performance')
            elif average_score >= 50:
                insights.append('Average performance')
            else:
                insights.append('Below average performance')
            
            return {
                'trend': 'Stable',
                'average': round(average_score, 1),
                'improvement_needed': average_score < 70,
                'insights': insights,
                'total_assessments': total_grades,
                'class_rank': 'N/A'
            }
        except:
            return {
                'trend': 'No Data',
                'average': 0,
                'improvement_needed': True,
                'insights': ['Analysis unavailable'],
                'total_assessments': 0,
                'class_rank': 'N/A'
            }

    @staticmethod
    def get_improvement_suggestions(student):
        suggestions = []
        try:
            recent_date = datetime.now().date() - timedelta(days=30)
            recent_grades = Grade.objects.filter(student=student, date__gte=recent_date)
            
            if recent_grades.exists():
                avg_grade = recent_grades.aggregate(avg=Avg('marks'))['avg']
                if avg_grade < 60:
                    suggestions.append("Focus on weak subjects")
                    suggestions.append("Form study groups")
                else:
                    suggestions.append("Maintain current performance")
            
            if not suggestions:
                suggestions = ["Continue your current study habits"]
        except:
            suggestions = ["Complete more assessments for insights"]
        
        return suggestions

class AttendancePatternAnalyzer:
    @staticmethod
    def analyze_attendance_patterns(student):
        try:
            recent_date = datetime.now().date() - timedelta(days=60)
            attendance_records = Attendance.objects.filter(student=student, date__gte=recent_date)
            
            if not attendance_records.exists():
                return {
                    'pattern': 'No Data',
                    'risk_level': 'Unknown',
                    'attendance_rate': 0,
                    'insights': ['No attendance data available'],
                    'predictions': [],
                    'total_days': 0,
                    'present_days': 0
                }
            
            total_days = attendance_records.count()
            present_days = attendance_records.filter(is_present=True).count()
            attendance_rate = (present_days / total_days) * 100 if total_days > 0 else 0
            
            if attendance_rate >= 95:
                risk_level = 'Low'
                insights = ['Excellent attendance record!']
            elif attendance_rate >= 85:
                risk_level = 'Medium'
                insights = ['Good attendance with minor concerns']
            else:
                risk_level = 'High'
                insights = ['Poor attendance affecting performance']
            
            predictions = []
            if attendance_rate < 80:
                predictions.append('High risk of continued poor attendance')
            else:
                predictions.append('Likely to maintain good attendance')
            
            return {
                'pattern': 'Regular',
                'risk_level': risk_level,
                'attendance_rate': round(attendance_rate, 1),
                'insights': insights,
                'predictions': predictions,
                'total_days': total_days,
                'present_days': present_days
            }
        except:
            return {
                'pattern': 'No Data',
                'risk_level': 'Unknown',
                'attendance_rate': 0,
                'insights': ['Analysis unavailable'],
                'predictions': [],
                'total_days': 0,
                'present_days': 0
            }

class PerformanceInsights:
    @staticmethod
    def get_comprehensive_analysis(student):
        try:
            risk_score = StudentPerformancePredictor.calculate_risk_score(student)
            risk_level, risk_class = StudentPerformancePredictor.get_risk_level(risk_score)
            grade_analysis = GradeAnalyzer.analyze_subject_performance(student)
            attendance_analysis = AttendancePatternAnalyzer.analyze_attendance_patterns(student)
            improvement_suggestions = GradeAnalyzer.get_improvement_suggestions(student)
            
            if risk_score >= 70:
                overall_status = {
                    'status': 'Needs Immediate Attention',
                    'color': 'danger',
                    'icon': 'fas fa-exclamation-triangle',
                    'message': 'This student requires immediate intervention.'
                }
            elif risk_score >= 40:
                overall_status = {
                    'status': 'Monitor Closely',
                    'color': 'warning',
                    'icon': 'fas fa-eye',
                    'message': 'Keep a close watch on progress.'
                }
            elif risk_score >= 20:
                overall_status = {
                    'status': 'Minor Concerns',
                    'color': 'info',
                    'icon': 'fas fa-info-circle',
                    'message': 'Some areas need attention.'
                }
            else:
                overall_status = {
                    'status': 'Excellent Progress',
                    'color': 'success',
                    'icon': 'fas fa-check-circle',
                    'message': 'Student is performing excellently.'
                }
            
            return {
                'risk_score': risk_score,
                'risk_level': risk_level,
                'risk_class': risk_class,
                'grade_analysis': grade_analysis,
                'attendance_analysis': attendance_analysis,
                'improvement_suggestions': improvement_suggestions,
                'overall_status': overall_status
            }
        except Exception as e:
            print(f"Analysis error: {e}")
            return {
                'risk_score': 50,
                'risk_level': 'Unknown',
                'risk_class': 'secondary',
                'grade_analysis': {
                    'trend': 'No Data',
                    'average': 0,
                    'improvement_needed': True,
                    'insights': ['Analysis unavailable'],
                    'total_assessments': 0,
                    'class_rank': 'N/A'
                },
                'attendance_analysis': {
                    'pattern': 'No Data',
                    'risk_level': 'Unknown',
                    'attendance_rate': 0,
                    'insights': ['Analysis unavailable'],
                    'predictions': [],
                    'total_days': 0,
                    'present_days': 0
                },
                'improvement_suggestions': ['Complete more activities for insights'],
                'overall_status': {
                    'status': 'Getting Started',
                    'color': 'info',
                    'icon': 'fas fa-info-circle',
                    'message': 'Complete more activities to unlock insights.'
                }
            }