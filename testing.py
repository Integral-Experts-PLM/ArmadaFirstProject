            payload = {
                "PersonIncidentEntry": incident_data.person_incident_entry,
                "OccurrenceDate": incident_data.occurrence_date.strftime("%Y-%m-%dT%H:%M:%S+02:00"),
                "configuration": incident_data.configuration,
                "UserText13": incident_data.user_text13_tail_number,
                "UserText17": incident_data.user_text17_mission_effect,

                "SystemTreeItem": equipment_data.failed_component,
                "SerialNumber": equipment_data.serial_number,
                "MeterReading": equipment_data.meter_reading_tsn,
                "TimeToFailure": equipment_data.time_to_failure_tso,
                "UserText10": equipment_data.user_text10_oem,
                "UserText11": equipment_data.analysis_team,

                "UserText4": location_details.user_text4_location,
                "UserText23": location_details.user_text24_address,
                "UserText25": location_details.user_text25_contact,
                "UserText22": location_details.user_text22_phone,
                "UserText21": location_details.user_text21_email,

                "OperatingMode": incident_details.operating_mode,
                "UserText2": incident_details.user_text2_initial_severity,
                "DescriptionIncident": incident_details.description_incident,
                # "AttachmentsIncidents": incident_details.attachments_incidents,

                "Configuration@odata.bind": f"Systems({system_id})/Configurations({configuration})",
                "SystemTreeItem@odata.bind": f"Systems({system_id})/TreeItems({tree_items})"
            }
