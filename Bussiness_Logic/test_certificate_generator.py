from services.certificate_generator import generate_certificate_pdf
import os

file_path = generate_certificate_pdf(
    learner_name="Sanjay Kumar",
    average_score=87.5,
    certificate_code="CERT-TEST1234-AB12CD"
)

print("Certificate generated at:", file_path)
assert os.path.exists(file_path)
print("File exists — test passed!")