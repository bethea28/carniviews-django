
# In your_app_name/management/commands/verify_companies.py

from django.core.management.base import BaseCommand
from company_app.models import UnverifiedCompany, Company
from django.utils import timezone

class Command(BaseCommand):
    help = 'Verifies unverified companies and moves them to the main Company model'

    def handle(self, *args, **options):
        unverified_companies = UnverifiedCompany.objects.all()
        self.stdout.write(self.style.SUCCESS(f'Found {unverified_companies.count()} unverified companies.'))

        verified_count = 0
        rejected_count = 0

        for unverified_company in unverified_companies:
            is_verified = self.run_verification_checks(unverified_company)

            if is_verified:
                Company.objects.create(
                    name=unverified_company.name,
                    address=unverified_company.address,
                    city=unverified_company.city,
                    state=unverified_company.state,
                    zip_code=unverified_company.zip_code,
                    hours=unverified_company.hours,
                    company_type=unverified_company.company_type,
                    photos=unverified_company.photos,
                    hoursData=unverified_company.hoursData,
                    description=unverified_company.description,
                    user=unverified_company.user,
                )
                # Optionally, handle associated images (move from UnverifiedCompany to Company)
                self.move_images(unverified_company, Company.objects.last()) # Assuming the last created is the one we just added
                unverified_company.delete()
                verified_count += 1
                self.stdout.write(self.style.SUCCESS(f'Verified and added: {unverified_company.name}'))
            else:
                # Consider marking as rejected instead of immediate deletion
                self.stdout.write(self.style.WARNING(f'Rejected: {unverified_company.name}'))
                unverified_company.delete()
                rejected_count += 1

        self.stdout.write(self.style.SUCCESS(f'Verification process complete. {verified_count} verified, {rejected_count} rejected.'))

    def run_verification_checks(self, company):
        # --- Implement your actual verification logic here ---
        # This is a placeholder example:
        if company.name and company.city and company.company_type:
            return True
        return False

    def move_images(self, unverified_company, company):
        from images_app.models import Image
        images = Image.objects.filter(unverified_company=unverified_company)
        for image in images:
            image.company = company
            image.unverified_company = None
            image.save()