<?php

/**
 * Heidi Health Scribe Sessions Widget
 *
 * @package   OpenEMR
 * @link      http://www.open-emr.org
 * @license   https://github.com/openemr/openemr/blob/master/LICENSE GNU General Public License 3
 */

require_once("../../globals.php");

use OpenEMR\Common\Csrf\CsrfUtils;

if (!CsrfUtils::verifyCsrfToken($_POST["csrf_token_form"])) {
    CsrfUtils::csrfNotVerified();
}

// Fetch Heidi sessions for this patient
$sessions = sqlStatement(
    "SELECT * FROM heidi_sessions WHERE pid = ? ORDER BY session_date DESC",
    [$pid]
);

$session_count = sqlNumRows($sessions);
?>

<div id='heidi_sessions'>
<?php if ($session_count == 0) { ?>
    <span class='text'>
        <?php echo xlt("No Heidi scribe sessions found for this patient."); ?>
    </span>
<?php } else { ?>
    <div class="heidi-sessions-list">
        <?php
        $index = 0;
        while ($session = sqlFetchArray($sessions)) {
            $index++;
            $session_id = attr($session['id']);
            $collapse_id = "heidi_session_" . $session_id;
            ?>
            <div class="heidi-session-item card mb-3">
                <div class="card-header" style="cursor: pointer; background-color: #f8f9fa;" 
                     data-toggle="collapse" data-target="#<?php echo $collapse_id; ?>" 
                     aria-expanded="false">
                    <strong><?php echo text($session['session_name']); ?></strong>
                    <br>
                    <small class="text-muted">
                        <i class="fa fa-calendar"></i> <?php echo text(date('M d, Y g:i A', strtotime($session['session_date']))); ?>
                        | <i class="fa fa-clock-o"></i> <?php echo text(gmdate('i:s', $session['duration'])); ?> min
                    </small>
                </div>
                <div id="<?php echo $collapse_id; ?>" class="collapse">
                    <div class="card-body">
                        <!-- AI Clinical Note -->
                        <div class="mb-3">
                            <h6 class="text-primary"><i class="fa fa-stethoscope"></i> <?php echo xlt('AI Clinical Note'); ?></h6>
                            <p><strong><?php echo text($session['consult_note_heading']); ?></strong></p>
                            <div class="border-left pl-3" style="white-space: pre-line; border-color: #007bff !important;">
                                <?php echo text($session['consult_note']); ?>
                            </div>
                        </div>
                        
                        <!-- Transcript -->
                        <div class="mb-3">
                            <h6 class="text-success"><i class="fa fa-comments"></i> <?php echo xlt('Session Transcript'); ?></h6>
                            <div class="border-left pl-3" style="max-height: 400px; overflow-y: auto; white-space: pre-line; border-color: #28a745 !important;">
                                <?php echo text($session['transcript']); ?>
                            </div>
                        </div>
                        
                        <!-- Session Metadata -->
                        <div class="text-muted small">
                            <i class="fa fa-info-circle"></i> 
                            <?php echo xlt('Session ID'); ?>: <?php echo text($session['heidi_session_id']); ?>
                        </div>
                    </div>
                </div>
            </div>
        <?php } ?>
    </div>
<?php } ?>
</div>

<style>
.heidi-session-item .card-header:hover {
    background-color: #e9ecef !important;
}
.heidi-session-item .collapse {
    transition: all 0.3s ease;
}
</style>
