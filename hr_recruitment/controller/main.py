from odoo import http
from odoo.http import request
from odoo.http import Response
import base64

class WebsiteFormController(http.Controller):
    @http.route('/referral/', type='http', auth="public", website=True)
    def website_form(self, **post):
        # Render the form template again
        return http.request.render('hr_recruitment.test_form_2')

    @http.route('/referral/website_thanks/', type='http', auth='public', website=True)
    def referral_website_thanks(self, **post):
        # Extract data from the form submission
        emp_name = post.get('emp_name')
        employee_email = post.get('employee_email')
        emp_id = post.get('emp_id')
        emp_account = post.get('emp_account')
        name = post.get('name')
        email = post.get('email')
        mobile_number = post.get('mobile_number')
        desired_position = post.get('desired_position')
        
        # Check for existing records
        existing_referrals = http.request.env['hr.referral'].sudo().search([
            '|',
            ('email', '=', email),
            ('mobile_number', '=', mobile_number),
            # ('record_ageing_ref', '<', 90)
        ])

        existing_referrals_applicant = http.request.env['hr.applicant'].sudo().search([
            '|',
            ('email_from', '=', email),
            ('x_mobile_number', '=', mobile_number),
            # ('record_ageing_ref', '<', 90)
        ])
        
        blacklisted_applicant = http.request.env['hr.blacklist'].sudo().search([
            ('email', '=', email),
            # ('record_ageing_ref', '<', 90)
        ])

        if existing_referrals or existing_referrals_applicant or blacklisted_applicant:
            error_message = "Duplicate entry found. Please ensure your data is unique."
            return http.request.render("hr_recruitment.duplicate_entry", {'error_message': error_message})

        # Handle the uploaded resume
        resume = http.request.httprequest.files.get('resume')
        resume_data = None
        if resume:
            resume_name = resume.filename
            resume_data = resume.read()

        # Find the user by name
        user_name = "Referral"
        user = http.request.env['res.users'].sudo().search([('name', '=', user_name)], limit=1)

        # Create a new hr.referral record with the extracted data
        referral_data = {
            'emp_name': emp_name,
            'employee_email': employee_email,
            'emp_id': emp_id,
            'emp_account': emp_account,
            'name': name,
            'email': email,
            'mobile_number': mobile_number,
            'desired_position': desired_position,
            'referral_ids': [(0, 0, {
                'name': resume_name,
                'res_model': 'hr.referral',
                'res_id': 0,
                'type': 'binary',
                'datas': base64.b64encode(resume_data),
                'mimetype': 'application/pdf',
            })] if resume_data else [],
            'user_id': user.id if user else False,
        }

        referral = http.request.env['hr.referral'].sudo().create(referral_data)

        # Continue with any additional actions or responses
        # For example, you can display a thank-you message
        return http.request.render("hr_recruitment.referral_thanks", {})


# class WebsiteFormController(http.Controller):
#     @http.route('/referral/', type='http', auth="public", website=True)
#     def website_form(self, **post):
#         # Render the form template again
#         return request.render('hr_recruitment.test_form_2')
#     @http.route('/referral/website_thanks/', type='http', auth='public', website=True)
#     def referral_website_thanks(self, **post):
#         # Extract data from the form submission
#         emp_name = post.get('emp_name')
#         employee_email = post.get('employee_email')
#         emp_id = post.get('emp_id')
#         emp_account = post.get('emp_account')
#         name = post.get('name')
#         email = post.get('email')
#         mobile_number = post.get('mobile_number')
#         desired_position = post.get('desired_position')
#         existing_email = request.env['hr.referral'].sudo().search_count([('record_ageing_ref', '<', 90), ('email', '=', email)])
#         existing_applicant_email = request.env['hr.applicant'].sudo().search_count([('record_ageing_ref', '<', 90), ('email_from', '=', email)])
#         existing_mobile = request.env['hr.referral'].sudo().search_count([('record_ageing_ref', '<', 90),('mobile_number', '=', mobile_number)])
#         existing_applicant_mobile = request.env['hr.applicant'].sudo().search_count([('record_ageing_ref', '<', 90),('x_mobile_number', '=', mobile_number)])
#         existing_form_email = request.env['hr.form'].sudo().search_count([('record_ageing_ref', '<', 90), ('email', '=', email)])
#         existing_form_mobile = request.env['hr.form'].sudo().search_count([('record_ageing_ref', '<', 90),('mobile_number', '=', mobile_number)])
        
#         if existing_email or existing_applicant_email or existing_form_email:
#             error_response = Response("The referral's email was already on the system, please try another.", status=400,
#                                       content_type='application/json')
#             return error_response
#         if existing_mobile or existing_applicant_mobile or existing_form_mobile:
#             error_response = Response("The referral's mobile number was already on the system, please try another.",
#                                       status=401,
#                                       content_type='application/json')
#             return error_response
#         if emp_name == 'N/A' or emp_name == 'n/a' or emp_name == 'N/A' or emp_name == 'n/a':
#             error_response = Response("N/A or n/a is not applicable, please try another.",
#                                       status=401,
#                                       content_type='application/json')
#             return error_response
#         if len(mobile_number) != 10:
#             error_response = Response(
#                 "The mobile number field is accepting 10 digits only. Please provide a valid mobile number.",
#                 status=401,
#                 content_type='application/json')
#             return error_response
#         # Handle the uploaded resume
#         resume = request.httprequest.files.get('resume')
#         resume_data = None
#         if resume:
#             resume_name = resume.filename
#             resume_data = resume.read()

#         # Find the user by name
#         user_name = "Referral"
#         user = request.env['res.users'].sudo().search([('name', '=', user_name)], limit=1)

#         # Create a new hr.referral record with the extracted data
#         referral_data = {
#             'emp_name': emp_name,
#             'employee_email': employee_email,
#             'emp_id': emp_id,
#             'emp_account': emp_account,
#             'name': name,
#             'email': email,
#             'mobile_number': mobile_number,
#             'desired_position': desired_position,
#             'referral_ids': [(0, 0, {
#                 'name': resume_name,
#                 'res_model': 'hr.referral',
#                 'res_id': 0,
#                 'type': 'binary',
#                 'datas': resume_data,
#                 'mimetype': 'application/pdf',
#                 'datas': base64.b64encode(resume_data),
#             })] if resume_data else [],
#             'user_id': user.id if user else False,
#         }

#         referral = request.env['hr.referral'].sudo().create(referral_data)

#         # Continue with any additional actions or responses
#         # For example, you can display a thank-you message
#         return request.render("hr_recruitment.referral_thanks", {})
    
class JobFormController(http.Controller):
    @http.route('/jobs/apply', type='http', auth="public", website=True)
    def website_form(self, **post):
        # Render the form template again
        return request.render('hr_recruitment.job_form_template')

    @http.route('/jobs/apply/job_thanks/', type='http', auth='public', website=True)
    def application_thanks(self, **post):
        # Extract data from the form submission
        name = post.get('name')
        email = post.get('email')
        mobile_number = post.get('mobile_number')
        linkedin = post.get('linkedin')
        existing_email = request.env['hr.form'].sudo().search([('email', '=', email)], limit=1)
        existing_applicant_email = request.env['hr.applicant'].sudo().search([('email_from', '=', email)], limit=1)
        existing_mobile = request.env['hr.form'].sudo().search([('mobile_number', '=', mobile_number)], limit=1)
        existing_applicant_mobile = request.env['hr.applicant'].sudo().search([('x_mobile_number', '=', mobile_number)],
                                                                              limit=1)
        existing_form_email = request.env['hr.form'].sudo().search([('email', '=', email)], limit=1)
        existing_form_mobile = request.env['hr.form'].sudo().search([('mobile_number', '=', mobile_number)],
                                                                              limit=1)

        if existing_email or existing_applicant_email or existing_form_email:
            error_response = Response("The applicant's email was already on the system, please try another.", status=400,
                                      content_type='application/json')
            return error_response
        if existing_mobile or existing_applicant_mobile or existing_form_mobile:
            error_response = Response("The applicant's mobile number was already on the system, please try another.",
                                      status=401,
                                      content_type='application/json')
            return error_response
        if name == 'N/A' or name == 'n/a' or name == 'N/A' or name == 'n/a':
            error_response = Response("N/A or n/a is not applicable, please try another.",
                                      status=401,
                                      content_type='application/json')
            return error_response
        if len(mobile_number) != 10:
            error_response = Response(
                "The mobile number field is accepting 10 digits only. Please provide a valid mobile number.",
                status=401,
                content_type='application/json')
            return error_response
        # Handle the uploaded resume
        resume = request.httprequest.files.get('attachment_id')
        resume_data = None
        if resume:
            resume_name = resume.filename
            resume_data = resume.read()

        # Find the user by name
        user_name = "Referral"
        user = request.env['res.users'].sudo().search([('name', '=', user_name)], limit=1)

        # Create a new hr.referral record with the extracted data
        applicant_data = {
            'name': name,
            'email': email,
            'mobile_number': mobile_number,
            'linkedin': linkedin,
            'attachment_id': [(0, 0, {
                'name': resume_name,
                'res_model': 'hr.form',
                'res_id': 0,
                'type': 'binary',
                'mimetype': 'application/pdf',
                'datas': base64.b64encode(resume_data),
            })] if resume_data else [],
            'user_id': user.id if user else False,
        }

        applicant = request.env['hr.form'].sudo().create(applicant_data)

        # Continue with any additional actions or responses
        # For example, you can display a thank-you message
        return request.render("hr_recruitment.application_thanks", {})    
