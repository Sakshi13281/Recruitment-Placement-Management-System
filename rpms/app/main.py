from rpms.dao.candidate_dao import CandidateDAO
from rpms.dao.job_dao import JobDAO
from rpms.dao.application_dao import ApplicationDAO

from rpms.model.candidate import Candidate

from rpms.service.candidate_service import CandidateService
from rpms.service.eligibility_service import EligibilityService
from rpms.service.application_service import ApplicationService
from rpms.service.report_service import ReportService
from rpms.service.activity_log_service import ActivityLogService


def print_menu():
    print("\n==================================")
    print("RECRUITMENT & PLACEMENT SYSTEM")
    print("==================================")
    print("1. View Candidates")
    print("2. Add Candidate")
    print("3. View Open Jobs")
    print("4. Apply for Job")
    print("5. Candidate Technology Report")
    print("6. Exit")


def main():
    candidate_dao = CandidateDAO()
    job_dao = JobDAO()
    application_dao = ApplicationDAO()

    candidate_service = CandidateService(candidate_dao)
    eligibility_service = EligibilityService()
    application_service = ApplicationService(
        candidate_dao,
        job_dao,
        application_dao,
        eligibility_service
    )

    report_service = ReportService()
    log_service = ActivityLogService()

    while True:
        print_menu()

        try:
            choice = int(input("Enter Choice: "))

            if choice == 1:
                candidates = candidate_service.get_all_candidates()
                if not candidates:
                    print("No candidates found.")
                for c in candidates:
                    print(c)

            elif choice == 2:
                candidate = Candidate(
                    candidate_code=input("Candidate Code: ").strip(),
                    full_name=input("Full Name: ").strip(),
                    email=input("Email: ").strip(),
                    mobile=input("Mobile: ").strip(),
                    qualification=input("Qualification: ").strip(),
                    passing_year=int(input("Passing Year: ")),
                    percentage=float(input("Percentage: ")),
                    backlog_count=int(input("Backlog Count: ")),
                    primary_technology=input("Primary Technology: ").strip()
                )

                candidate_id = candidate_service.add_candidate(candidate)
                print(f"Candidate created. ID = {candidate_id}")
                log_service.log(f"Candidate created: {candidate.candidate_code}")

            elif choice == 3:
                jobs = job_dao.find_open_jobs()
                if not jobs:
                    print("No open jobs found.")
                for job in jobs:
                    print(job)

            elif choice == 4:
                candidate_id = int(input("Candidate ID: "))
                job_id = int(input("Job ID: "))
                application_id = application_service.apply_for_job(candidate_id, job_id)
                print(f"Application created. ID = {application_id}")
                log_service.log(
                    f"Application created: candidate={candidate_id}, job={job_id}"
                )

            elif choice == 5:
                rows = report_service.candidate_count_by_technology()
                if not rows:
                    print("No report data found.")
                for technology, total in rows:
                    print(f"{technology}: {total}")

            elif choice == 6:
                print("Application closed.")
                break

            else:
                print("Invalid choice.")

        except (EOFError, KeyboardInterrupt):
            print("\nApplication closed.")
            break

        except Exception as exc:
            print("ERROR:", exc)


if __name__ == "__main__":
    main()
