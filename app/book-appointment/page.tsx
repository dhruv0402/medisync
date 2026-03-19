"use client";

import { useState, useEffect } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import ProtectedRoute from "@/components/ProtectedRoute";
import LoadingSpinner from "@/components/LoadingSpinner";
import { appointmentAPI } from "@/lib/api";
import { useRouter } from "next/navigation";

interface Doctor {
  id: string;
  name: string;
  specialization: string;
}

interface Slot {
  id: string;
  time: string;
  available: boolean;
}

export default function BookAppointmentPage() {
  const router = useRouter();
  const [departments, setDepartments] = useState([
    { id: "1", name: "Cardiology" },
    { id: "2", name: "Orthopedics" },
    { id: "3", name: "Pediatrics" },
    { id: "4", name: "Neurology" },
  ]);
  const [step, setStep] = useState(1);
  const [selectedDept, setSelectedDept] = useState("");
  const [selectedDoctor, setSelectedDoctor] = useState("");
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedSlot, setSelectedSlot] = useState("");
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [slots, setSlots] = useState<Slot[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Fetch doctors when department is selected
  useEffect(() => {
    if (selectedDept) {
      const fetchDoctors = async () => {
        try {
          setLoading(true);
          const data = await appointmentAPI.getDoctors(selectedDept);
          setDoctors(data.doctors || []);
        } catch (err) {
          setError("Failed to fetch doctors");
        } finally {
          setLoading(false);
        }
      };
      fetchDoctors();
    }
  }, [selectedDept]);

  // Fetch slots when doctor and date are selected
  useEffect(() => {
    if (selectedDoctor && selectedDate) {
      const fetchSlots = async () => {
        try {
          setLoading(true);
          const data = await appointmentAPI.getSlots(selectedDoctor, selectedDate);
          setSlots(data.slots || []);
        } catch (err) {
          setError("Failed to fetch slots");
        } finally {
          setLoading(false);
        }
      };
      fetchSlots();
    }
  }, [selectedDoctor, selectedDate]);

  const handleBooking = async () => {
    if (!selectedSlot) {
      setError("Please select a time slot");
      return;
    }

    try {
      setLoading(true);
      setError("");
      await appointmentAPI.bookAppointment({
        doctor_id: selectedDoctor,
        slot_id: selectedSlot,
        date: selectedDate,
      });
      setSuccess("Appointment booked successfully!");
      setTimeout(() => {
        router.push("/appointments");
      }, 2000);
    } catch (err) {
      setError("Failed to book appointment");
    } finally {
      setLoading(false);
    }
  };

  const getTomorrow = () => {
    const date = new Date();
    date.setDate(date.getDate() + 1);
    return date.toISOString().split("T")[0];
  };

  const getMaxDate = () => {
    const date = new Date();
    date.setDate(date.getDate() + 30);
    return date.toISOString().split("T")[0];
  };

  return (
    <ProtectedRoute requiredRole="patient">
      <DashboardLayout>
        <div className="max-w-3xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-foreground mb-2">Book an Appointment</h1>
            <p className="text-secondary">Follow the steps to schedule your visit</p>
          </div>

          {/* Progress Indicator */}
          <div className="flex gap-4 mb-8">
            {[1, 2, 3, 4].map((s) => (
              <div
                key={s}
                className={`flex-1 h-2 rounded-full ${
                  s <= step ? "bg-primary" : "bg-border"
                }`}
              />
            ))}
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-error text-error rounded-lg">
              {error}
            </div>
          )}

          {success && (
            <div className="mb-4 p-4 bg-green-50 border border-success text-success rounded-lg">
              {success}
            </div>
          )}

          <div className="card p-8">
            {/* Step 1: Select Department */}
            {step === 1 && (
              <div>
                <h2 className="text-xl font-bold text-foreground mb-4">Select Department</h2>
                <div className="grid grid-cols-2 gap-4">
                  {departments.map((dept) => (
                    <button
                      key={dept.id}
                      onClick={() => {
                        setSelectedDept(dept.id);
                        setStep(2);
                      }}
                      className={`p-4 border-2 rounded-lg font-medium transition-all ${
                        selectedDept === dept.id
                          ? "border-primary bg-blue-50"
                          : "border-border hover:border-primary"
                      }`}
                    >
                      {dept.name}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Step 2: Select Doctor */}
            {step === 2 && (
              <div>
                <h2 className="text-xl font-bold text-foreground mb-4">Select Doctor</h2>
                {loading ? (
                  <LoadingSpinner />
                ) : doctors.length === 0 ? (
                  <p className="text-secondary text-center py-8">No doctors available</p>
                ) : (
                  <div className="space-y-3">
                    {doctors.map((doctor) => (
                      <button
                        key={doctor.id}
                        onClick={() => {
                          setSelectedDoctor(doctor.id);
                          setStep(3);
                        }}
                        className={`w-full p-4 border-2 rounded-lg text-left transition-all ${
                          selectedDoctor === doctor.id
                            ? "border-primary bg-blue-50"
                            : "border-border hover:border-primary"
                        }`}
                      >
                        <p className="font-semibold text-foreground">{doctor.name}</p>
                        <p className="text-sm text-secondary">{doctor.specialization}</p>
                      </button>
                    ))}
                  </div>
                )}
                <button
                  onClick={() => setStep(1)}
                  className="mt-4 btn-outline"
                >
                  Back
                </button>
              </div>
            )}

            {/* Step 3: Select Date */}
            {step === 3 && (
              <div>
                <h2 className="text-xl font-bold text-foreground mb-4">Select Date</h2>
                <input
                  type="date"
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                  min={getTomorrow()}
                  max={getMaxDate()}
                  className="input-field mb-4"
                />
                {selectedDate && (
                  <button
                    onClick={() => setStep(4)}
                    className="w-full btn-primary"
                  >
                    Continue
                  </button>
                )}
                <button
                  onClick={() => setStep(2)}
                  className="w-full mt-2 btn-outline"
                >
                  Back
                </button>
              </div>
            )}

            {/* Step 4: Select Slot */}
            {step === 4 && (
              <div>
                <h2 className="text-xl font-bold text-foreground mb-4">Select Time Slot</h2>
                {loading ? (
                  <LoadingSpinner />
                ) : slots.length === 0 ? (
                  <p className="text-secondary text-center py-8">No slots available for this date</p>
                ) : (
                  <div className="grid grid-cols-3 gap-3 mb-6">
                    {slots.map((slot) => (
                      <button
                        key={slot.id}
                        onClick={() => setSelectedSlot(slot.id)}
                        disabled={!slot.available}
                        className={`p-3 border-2 rounded-lg font-medium transition-all ${
                          !slot.available
                            ? "opacity-50 cursor-not-allowed border-border"
                            : selectedSlot === slot.id
                            ? "border-primary bg-blue-50"
                            : "border-border hover:border-primary"
                        }`}
                      >
                        {slot.time}
                      </button>
                    ))}
                  </div>
                )}
                {selectedSlot && (
                  <button
                    onClick={handleBooking}
                    disabled={loading}
                    className="w-full btn-primary disabled:opacity-50"
                  >
                    {loading ? "Booking..." : "Confirm Booking"}
                  </button>
                )}
                <button
                  onClick={() => setStep(3)}
                  className="w-full mt-2 btn-outline"
                >
                  Back
                </button>
              </div>
            )}
          </div>
        </div>
      </DashboardLayout>
    </ProtectedRoute>
  );
}
